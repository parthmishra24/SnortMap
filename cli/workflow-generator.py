import json
import questionary
from rich.console import Console
from rich.panel import Panel
from utils.loader import load_attack_vectors

console = Console()

OBJECTIVES = {
    "Credential Dumping": ["Kerberoasting", "AS-REP Roasting", "DCSync Attack"],
    "Privilege Escalation": ["Kerberoasting", "ACL enumeration", "Golden Ticket Attack"],
    "Lateral Movement": ["Password spraying", "Subdomain enumeration", "Phishing campaigns"],
    "Persistence": ["Golden Ticket Attack", "DCSync Attack"]
}

def generate_workflow(domain, access, objective, attack_data):
    results = []
    available = attack_data.get(domain, {}).get(access, {})

    for step in OBJECTIVES.get(objective, []):
        if step in available:
            tools = available[step].get("tools", {})
            for tool, tool_data in tools.items():
                results.append({
                    "attack": step,
                    "tool": tool,
                    "command": tool_data.get("command"),
                    "link": tool_data.get("link")
                })
                break  # Only show one tool per attack
    return results

def main():
    console.print("[bold cyan]🎯 SnortMap: Red Team Ops Workflow Generator[/bold cyan]\n")
    attack_data = load_attack_vectors()

    domain = questionary.select("Select Target Domain:", choices=list(attack_data.keys())).ask()
    if not domain:
        console.print("[red]Domain selection cancelled.[/red]")
        return

    access_levels = list(attack_data[domain].keys())
    access = questionary.select("Select Access Level:", choices=access_levels).ask()
    if not access:
        console.print("[red]Access level selection cancelled.[/red]")
        return

    objective = questionary.select("Select Objective:", choices=list(OBJECTIVES.keys())).ask()
    if not objective:
        console.print("[red]Objective selection cancelled.[/red]")
        return

    console.print(f"\n[bold green]🔥 Workflow for {domain} | Access: {access} | Goal: {objective}[/bold green]\n")

    plan = generate_workflow(domain, access, objective, attack_data)

    if not plan:
        console.print("[yellow]No relevant attack workflow found for this combination.[/yellow]")
        return

    for i, step in enumerate(plan, 1):
        panel = Panel.fit(
            f"[bold yellow]{step['attack']}[/bold yellow]\n"
            f"[bold magenta]Tool:[/bold magenta] {step['tool']}\n"
            f"[bold green]Command:[/bold green] {step['command']}\n"
            f"[bold blue]More Info:[/bold blue] {step['link']}",
            title=f"Step {i}",
            border_style="cyan"
        )
        console.print(panel)

if __name__ == "__main__":
    main()