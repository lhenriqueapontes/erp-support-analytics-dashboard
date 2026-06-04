from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from metrics import calculate_kpis, tickets_by_module


def export_reports(input_path: str, output_dir: str = "reports") -> None:
    df = pd.read_csv(input_path)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    kpis = calculate_kpis(df)
    pd.DataFrame([kpis]).to_csv(output / "kpi_summary.csv", index=False)
    tickets_by_module(df).to_csv(output / "module_summary.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/synthetic_erp_tickets.csv")
    parser.add_argument("--output-dir", default="reports")
    args = parser.parse_args()
    export_reports(args.input, args.output_dir)
    print(f"Reports saved to {args.output_dir}")


if __name__ == "__main__":
    main()
