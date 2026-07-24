from typing import Dict, Optional

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


def print_domains(domains_criticality: Optional[Dict[str, int]] = None) -> None:
    if not domains_criticality:
        domains_criticality = {
            "example.com": 0,
            "example.org": 1,
            "example.net": 2,
            "example.edu": 3,
            "example.gov": 4
        }

    # Сортируем по критичности (числовому значению)
    sorted_domains = sorted(domains_criticality.items(
    ), key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0)

    max_domain_length = max(len(domain) for domain, _ in sorted_domains)
    max_column_length = max(max_domain_length, 10)

    table = Table(title="Domains List", style="cyan",
                  title_style="bold", width=max_column_length * 2 + 10)
    table.add_column("Domains", style="bold",
                     width=max_column_length + 10, justify="center")
    table.add_column("Criticality", style="bold",
                     width=max_column_length + 10, justify="center")

    criticality_values = ["Legitimate", "Low", "Medium", "High", "Critical"]
    criticality_colors = {
        "Legitimate": "green",
        "Low": "blue",
        "Medium": "cyan",
        "High": "yellow",
        "Critical": "red"
    }

    for domain, criticality_value in sorted_domains:
        # ==== ЗАЩИТА ====
        if not isinstance(criticality_value, int):
            # Если не число, логируем и приравниваем к 0 (или можно к 1)
            console.log(
                f"[yellow]Warning: non-integer criticality for {domain}: {criticality_value}, setting to 0[/]")
            criticality_value = 0
        # Если число вне диапазона, тоже корректируем
        if criticality_value < 0 or criticality_value >= len(criticality_values):
            console.log(
                f"[yellow]Warning: criticality {criticality_value} out of range for {domain}, clamping to 0[/]")
            criticality_value = 0
        # ==================

        criticality_name = criticality_values[criticality_value]
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
# print_banner()
# print_domains({"123.ru":"0", "qwe.com":"3"})
