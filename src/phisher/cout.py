from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress
from time import sleep

console = Console()


def print_banner():
    # Write name of the utility
    banner = """
██████╗░██╗░░██╗██╗░██████╗██╗░░██╗███████╗██████╗░
██╔══██╗██║░░██║██║██╔════╝██║░░██║██╔════╝██╔══██╗
██████╔╝███████║██║╚█████╗░███████║█████╗░░██████╔╝
██╔═══╝░██╔══██║██║░╚═══██╗██╔══██║██╔══╝░░██╔══██╗
██║░░░░░██║░░██║██║██████╔╝██║░░██║███████╗██║░░██║
╚═╝░░░░░╚═╝░░╚═╝╚═╝╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
             """
    banner_text = Text(banner, style="bold red", justify="center")
    banner_panel = Panel(banner_text, title="Identify Phishing and Shadow-IT Resources",
                         subtitle="[red]Stop Fraudulent Activities[/red]", width=80)
    console.print(banner_panel)

    # Display the utility version
    version = "1.0.1#dev"
    console.print(Text(f"Version: {version}",
                  style="bold green", justify="center"))

    # Display the team name
    console.print(Text("Team: Knights of the Round Table",
                  style="bold", justify="center"))

    # Print reference
    console.print(Text(
        "Usage: python phisher [input_file] [api_key]", style="bold", justify="center"))

def print_domains(domains_criticality=None):
    if not domains_criticality:
        domains_criticality = {
            "example.com": "Legitimate",
            "example.org": "Low",
            "example.net": "Medium",
            "example.edu": "High",
            "example.gov": "Critical"
        }

    # Sort domains by criticality level
    sorted_domains = sorted(domains_criticality.items(), key=lambda x: x[1])

    # Determine maximum lengths for domain and criticality for proper table formatting
    max_domain_length = max(len(domain) for domain, _ in sorted_domains)
    max_column_length = max(max_domain_length, 10)

    # Create a table with appropriate width and column formatting
    table = Table(title="Domains List", style="cyan",
                  title_style="bold", width=max_column_length * 2 + 10)
    table.add_column("Domains", style="bold",
                     width=max_column_length + 10, justify="center")
    table.add_column("Criticality", style="bold",
                     width=max_column_length + 10, justify="center")

    # Define criticality values
    criticality_values = ["Legitimate", "Low", "Medium", "High", "Critical"]

    # Map criticality values to color gradients
    criticality_colors = {
        "Legitimate": "green",
        "Low": "blue",
        "Medium": "cyan",
        "High": "yellow",
        "Critical": "red"
    }

    # Populate the table with domain-criticality pairs with colored text
    for domain, criticality_value in sorted_domains:
        criticality_name = criticality_values[int(criticality_value)]
        criticality_label = f"[{criticality_colors[criticality_name]}]{criticality_name}[/]"
        table.add_row(domain, criticality_label)

    console.print(table)


def print_percents(total: int):
    with Progress() as progress:
        task = progress.add_task("[green]Searching resources...", total=total)
        while not progress.finished:
            for i in range(1, total + 1):
                progress.update(task, completed=i)
                sleep(0.1)
    console.print()


# Example usage:
#print_banner()
#print_domains({"123.ru":"0", "qwe.com":"3"})
