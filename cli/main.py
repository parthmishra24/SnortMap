import json
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import pyperclip
from utils.loader import load_attack_vectors

console = Console()

def print_attack_info(domain, vectors):
    if not vectors:
        console.print("[yellow]Warning: No attack vectors found for this selection.[/yellow]")
        return False

    attack_choices = []
    attack_map = {}

    for atk, details in vectors.items():
        if isinstance(details, dict) and 'tools' in details:
            label = f"{atk} - {details.get('description', '')}"
            attack_choices.append(label)
            attack_map[label] = atk
        else:
            attack_choices.append(atk)
            attack_map[atk] = atk

    attack_choice_str = questionary.select(
        "Select an attack to explore further:",
        choices=attack_choices
    ).ask()

    if not attack_choice_str:
        console.print("[red]Cancelled by user.[/red]")
        return False

    attack_choice = attack_map[attack_choice_str]
    attack_block = vectors[attack_choice]

    if isinstance(attack_block, dict):
        tools = attack_block.get("tools", attack_block)
        if isinstance(tools, dict):
            tool_choice = questionary.select(
                "Select a tool to view details:",
                choices=list(tools.keys())
            ).ask()

            if not tool_choice:
                console.print("[red]Cancelled by user.[/red]")
                return False

            tool_data = tools[tool_choice]
            tool_name = tool_choice
            command = tool_data.get("command", "No command available.")
            link = tool_data.get("link", "No reference link provided.")

            panel = Panel.fit(
                f"[bold magenta]Tool:[/bold magenta] {tool_name}\n"
                f"[bold yellow]Command:[/bold yellow] [green]{command}[/green]\n"
                f"[bold blue]Link:[/bold blue] {link}",
                title="Attack Step",
                border_style="cyan"
            )
            console.print(panel)

            if questionary.confirm("Copy this command to clipboard?").ask():
                pyperclip.copy(command)
                console.print("[dim]Command copied to clipboard[/dim]")

    return True

def search_index(data, query):
    results = []
    query = query.lower()
    for entry in data:
        if any(query in str(value).lower() for value in entry.values()):
            results.append(entry)
    return results

def display_results(results):
    if not results:
        console.print("[bold red]No matches found.[/bold red]")
        return False

    table = Table(show_lines=True)
    table.add_column("Domain", style="cyan", no_wrap=True)
    table.add_column("Access Level", style="magenta")
    table.add_column("Attack", style="bold yellow")
    table.add_column("Tool", style="green")
    table.add_column("Command", style="white")
    table.add_column("Link", style="blue")

    for item in results:
        table.add_row(
            item["domain"],
            item["access_level"],
            item["attack"],
            item["tool"],
            item["command"],
            item["link"]
        )

    console.print(table)
    return True

def restart_or_exit():
    next_action = questionary.select("Would you like to:", choices=["Start Over", "Exit"]).ask()
    if next_action == "Start Over":
        main()
    else:
        console.print("[bold red]Goodbye from SnortMap![/bold red]")
        exit()

def run_search():
    try:
        with open("data/search_index_attack_vectors.json", "r") as f:
            index = json.load(f)
    except Exception as e:
        console.print(f"[red]Error loading search index: {e}[/red]")
        return False

    query = questionary.text("Enter search keyword:").ask()
    if not query:
        console.print("[red]No input provided.[/red]")
        return False

    matches = search_index(index, query)
    return display_results(matches)

def main():
    attack_data = load_attack_vectors()

    console.print("""
[bold cyan]
╔═════════════════════════════════════════════╗
║               SnortMap CLI                 ║
╠═════════════════════════════════════════════╣
║  Explore domains • Simulate attack paths   ║
║  Learn tools • Copy payloads instantly     ║
╚═════════════════════════════════════════════╝
[/bold cyan]
""")

    choice = questionary.select(
        "What would you like to do?",
        choices=["Explore by Domain", "Search by Keyword"]
    ).ask()

    if not choice:
        console.print("[red]Cancelled by user.[/red]")
        return

    if choice == "Search by Keyword":
        if run_search():
            restart_or_exit()
        return

    domain = questionary.select(
        "Select a domain to explore:",
        choices=list(attack_data.keys())
    ).ask()

    if not domain:
        console.print("[red]No domain selected. Exiting.[/red]")
        return

    access_levels = list(attack_data[domain].keys())

    access = questionary.select(
        f"What is your access level in [bold]{domain}[/bold]?",
        choices=access_levels
    ).ask()

    if not access:
        console.print("[red]No access level selected. Exiting.[/red]")
        return

    vectors = attack_data[domain][access]
    if print_attack_info(domain, vectors):
        restart_or_exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting on user interrupt.[/red]")
