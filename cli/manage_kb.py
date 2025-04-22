import json
import os
import sys
from pathlib import Path
import questionary
from questionary import Choice
from rich.console import Console
from rapidfuzz import process, fuzz
import signal

console = Console()

KB_PATH = "data/attack_vectors.json"
INDEX_PATH = "data/search_index_attack_vectors.json"

def handle_sigint(signum, frame):
    console.print("\n[red]❌ Exiting tool immediately on user interrupt (Ctrl+C).[/red]")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_sigint)

def prompt_or_exit(prompt):
    value = prompt.ask()
    if value is None:
        console.print("[red]❌ Cancelled by user.[/red]")
        sys.exit(0)
    return value

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def update_search_index(data):
    search_index = []
    for domain, access_data in data.items():
        for access, attacks in access_data.items():
            for attack_name, attack_info in attacks.items():
                description = attack_info.get("description", "")
                tools = attack_info.get("tools", {})
                for tool_name, tool in tools.items():
                    search_index.append({
                        "domain": domain,
                        "access_level": access,
                        "attack": attack_name,
                        "description": description,
                        "tool": tool_name,
                        "command": tool.get("command", ""),
                        "link": tool.get("link", "")
                    })
    save_json(INDEX_PATH, search_index)
    console.print("[green]✔ Search index updated.[/green]")

def autocomplete_from(options, prompt="Choose:"):
    user_input = prompt_or_exit(questionary.text(prompt))
    best_matches = process.extract(user_input, options, scorer=fuzz.WRatio, limit=5)
    choice = prompt_or_exit(questionary.select("Select closest match:", choices=[Choice(m[0]) for m in best_matches]))
    return choice

def add_entry():
    console.print("[bold cyan]➕ Add a new knowledge base entry[/bold cyan]")
    kb = load_json(KB_PATH)

    domain = prompt_or_exit(questionary.text("Domain (e.g., Web Application Security, Active Directory)"))
    access = prompt_or_exit(questionary.text("Access Level (e.g., User, Admin, No Access)"))
    attack = prompt_or_exit(questionary.text("Attack Name"))

    if domain in kb and access in kb[domain] and attack in kb[domain][access]:
        console.print("[red]❗ Entry already exists. Use --edit to modify it.[/red]")
        return

    description = prompt_or_exit(questionary.text("Attack Description"))
    tool = prompt_or_exit(questionary.text("Tool Name"))
    command = prompt_or_exit(questionary.text("Command Example"))
    link = prompt_or_exit(questionary.text("Reference Link"))

    kb.setdefault(domain, {}).setdefault(access, {})[attack] = {
        "description": description,
        "tools": {
            tool: {
                "command": command,
                "link": link
            }
        }
    }

    save_json(KB_PATH, kb)
    update_search_index(kb)
    console.print("[bold green]✅ Entry added successfully![/bold green]")

def edit_entry():
    console.print("[bold yellow]✏️ Edit an existing entry[/bold yellow]")
    kb = load_json(KB_PATH)

    domain = autocomplete_from(list(kb.keys()), "Search for domain:")
    access = autocomplete_from(list(kb[domain].keys()), "Search for access level:")
    attack = autocomplete_from(list(kb[domain][access].keys()), "Search for attack:")
    entry = kb[domain][access][attack]

    new_description = prompt_or_exit(questionary.text("New Description", default=entry.get("description", "")))

    tools = entry.get("tools", {})
    tool = autocomplete_from(list(tools.keys()), "Search for tool to edit:")
    tool_data = tools[tool]

    new_command = prompt_or_exit(questionary.text("New Command", default=tool_data.get("command", "")))
    new_link = prompt_or_exit(questionary.text("New Link", default=tool_data.get("link", "")))

    entry["description"] = new_description
    entry["tools"][tool] = {
        "command": new_command,
        "link": new_link
    }

    save_json(KB_PATH, kb)
    update_search_index(kb)
    console.print("[bold green]✅ Entry updated.[/bold green]")

def delete_entry():
    console.print("[bold red]🗑 Delete an entry[/bold red]")
    kb = load_json(KB_PATH)

    domain = autocomplete_from(list(kb.keys()), "Search for domain:")
    access = autocomplete_from(list(kb[domain].keys()), "Search for access level:")
    attack = autocomplete_from(list(kb[domain][access].keys()), "Search for attack to delete:")

    if prompt_or_exit(questionary.confirm(f"Are you sure you want to delete attack '{attack}' from {domain} → {access}?")):
        del kb[domain][access][attack]
        if not kb[domain][access]:
            del kb[domain][access]
        if not kb[domain]:
            del kb[domain]

        save_json(KB_PATH, kb)
        update_search_index(kb)
        console.print("[bold green]✅ Entry deleted.[/bold green]")

if __name__ == "__main__":
    try:
        if "--add" in sys.argv:
            add_entry()
        elif "--edit" in sys.argv:
            edit_entry()
        elif "--delete" in sys.argv:
            delete_entry()
        else:
            console.print("""
[cyan]Knowledge Base Manager[/cyan]
Usage:
  python manage_kb.py --add      # Add new entry
  python manage_kb.py --edit     # Edit existing entry
  python manage_kb.py --delete   # Delete existing entry
""")
    except KeyboardInterrupt:
        handle_sigint(None, None)