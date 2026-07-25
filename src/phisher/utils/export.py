# phisher/utils/export.py
import json
import csv
from typing import Dict


def export_domains(domains: Dict[str, int], fmt: str, filepath: str = None):
    if not filepath:
        filepath = f"results.{fmt}"
    if fmt == "json":
        with open(filepath, "w") as f:
            json.dump(domains, f, indent=2)
    elif fmt == "csv":
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["domain", "criticality"])
            for domain, crit in sorted(domains.items(), key=lambda x: x[1], reverse=True):
                writer.writerow([domain, crit])
    print(f"Results saved to {filepath}")
