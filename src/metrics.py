"""Basic KPI calculations for synthetic ERP support tickets."""
from __future__ import annotations

import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    return {
        "tickets": int(len(df)),
        "avg_first_response_hours": round(float(df["first_response_hours"].mean()), 2),
        "avg_resolution_hours": round(float(df["resolution_hours"].mean()), 2),
        "sla_rate": round(float(df["sla_met"].mean()), 4),
        "critical_tickets": int((df["priority"] == "Critical").sum()),
    }


def tickets_by_module(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("module", as_index=False).agg(
        tickets=("ticket_id", "count"),
        avg_resolution_hours=("resolution_hours", "mean"),
        sla_rate=("sla_met", "mean"),
    ).round(2)
