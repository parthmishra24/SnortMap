import json
import argparse
import questionary
from pathlib import Path

DATA_PATH = Path("../data/attack_vectors.json")

def load_data():
    if not DATA_PATH.exists():
        print("attack_vectors.json not found. Creating a new one.")
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        DATA_PATH.write_text("{}")
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print("\n✅ Entry successfully saved.")

def prompt_for_domain(data):
    if not data:
        print("No existing domains found. Please add a new one.")
        return questionary.text("Enter new domain:").ask()
    if questionary.confirm("Do you want to add a new domain?").ask():
        return questionary.text("Enter new domain:").ask()
    else:
        return questionary.select("Select an existing domain:", choices=list(data.keys())).ask()

def prompt_for_access_level(domain_data):
    if not domain_data:
        print("No existing access levels found. Please add a new one.")
        return questionary.text("Enter new access level:").ask()
    if questionary.confirm("Do you want to add a new access level?").ask():
        return questionary.text("Enter new access level:").ask()
    else:
        return questionary.select("Select an existing access level:", choices=list(domain_data.keys())).ask()

def add_entry():
    data = load_data()

    domain = prompt_for_domain(data)
    if domain not in data:
        data[domain] = {}

    access = prompt_for_access_level(data[domain])
    if access not in data[domain]:
        data[domain][access] = {}

    attack = questionary.text("Enter attack name:").ask()
    description = questionary.text("Enter description for this attack:").ask()
    tool = questionary.text("Enter tool name:").ask()
    command = questionary.text("Enter command:").ask()
    link = questionary.text("Enter reference link (optional):").ask()

    if attack not in data[domain][access]:
        data[domain][access][attack] = {
            "description": description,
            "tools": {}
        }

    data[domain][access][attack]["tools"][tool] = {
        "command": command,
        "link": link
    }

    save_data(data)

def delete_entry():
    data = load_data()
    domain = questionary.select("Select domain:", choices=list(data.keys())).ask()
    access = questionary.select("Select access level:", choices=list(data[domain].keys())).ask()
    attack = questionary.select("Select attack to delete:", choices=list(data[domain][access].keys())).ask()

    del data[domain][access][attack]

    if not data[domain][access]:
        del data[domain][access]
    if not data[domain]:
        del data[domain]

    save_data(data)

def edit_entry():
    data = load_data()
    domain = questionary.select("Select domain:", choices=list(data.keys())).ask()
    access = questionary.select("Select access level:", choices=list(data[domain].keys())).ask()
    attack = questionary.select("Select attack to edit:", choices=list(data[domain][access].keys())).ask()

    description = questionary.text("Edit description:", default=data[domain][access][attack]["description"]).ask()
    tool = questionary.select("Select tool to edit:", choices=list(data[domain][access][attack]["tools"].keys())).ask()
    command = questionary.text("Edit command:", default=data[domain][access][attack]["tools"][tool]["command"]).ask()
    link = questionary.text("Edit reference link:", default=data[domain][access][attack]["tools"][tool]["link"]).ask()

    data[domain][access][attack]["description"] = description
    data[domain][access][attack]["tools"][tool] = {"command": command, "link": link}

    save_data(data)

def main():
    parser = argparse.ArgumentParser(description="Manage SnortMap Knowledge Base")
    parser.add_argument("--add", action="store_true", help="Add new attack method")
    parser.add_argument("--delete", action="store_true", help="Delete an attack method")
    parser.add_argument("--edit", action="store_true", help="Edit an existing attack method")
    args = parser.parse_args()

    if args.add:
        add_entry()
    elif args.delete:
        delete_entry()
    elif args.edit:
        edit_entry()

if __name__ == "__main__":
    main()