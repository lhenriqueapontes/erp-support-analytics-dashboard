"""Generate synthetic ERP support tickets for portfolio analytics.

This script does not use real company, client or ERP data.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

MODULES = ["Accounting", "Fiscal", "Payroll", "Inventory", "Finance", "Reports"]
CATEGORIES = ["User question", "Configuration", "Bug", "Integration", "Performance", "Training"]
PRIORITIES = ["Low", "Medium", "High", "Critical"]


def generate_tickets(n: int = 500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    created = pd.date_range("2025-01-01", periods=n, freq="12H")
    priority = rng.choice(PRIORITIES, size=n, p=[0.35, 0.40, 0.20, 0.05])
    first_response_hours = rng.gamma(shape=2.0, scale=1.5, size=n).round(2)
    resolution_hours = (first_response_hours + rng.gamma(shape=3.0, scale=6.0, size=n)).round(2)
    sla_target = np.select(
        [priority == "Critical", priority == "High", priority == "Medium"],
        [8, 24, 48],
        default=72,
    )
    return pd.DataFrame(
        {
            "ticket_id": [f"ERP-{i:05d}" for i in range(1, n + 1)],
            "created_at": created,
            "module": rng.choice(MODULES, size=n),
            "category": rng.choice(CATEGORIES, size=n),
            "priority": priority,
            "first_response_hours": first_response_hours,
            "resolution_hours": resolution_hours,
            "sla_target_hours": sla_target,
            "sla_met": resolution_hours <= sla_target,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=500)
    parser.add_argument("--output", default="data/synthetic_erp_tickets.csv")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_tickets(args.rows).to_csv(output, index=False)
    print(f"Saved synthetic tickets to {output}")


if __name__ == "__main__":
    main()
