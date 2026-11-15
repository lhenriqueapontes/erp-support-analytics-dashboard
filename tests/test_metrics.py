"""Regression tests for the synthetic ERP support ticket pipeline."""
from __future__ import annotations

import pandas as pd
import pytest

from src.generate_tickets import generate_tickets
from src.metrics import calculate_kpis, tickets_by_module


def test_generator_is_reproducible_and_unique() -> None:
    first = generate_tickets(n=100, seed=123)
    second = generate_tickets(n=100, seed=123)
    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 100
    assert first["ticket_id"].is_unique
    assert first["created_at"].notna().all()


def test_generated_sla_matches_resolution_and_target() -> None:
    df = generate_tickets(n=200, seed=34)
    assert (df["resolution_hours"] >= df["first_response_hours"]).all()
    assert (df["sla_target_hours"] > 0).all()
    assert df["sla_met"].equals(df["resolution_hours"] <= df["sla_target_hours"])


def test_kpis_calculate_correct_values() -> None:
    df = pd.DataFrame(
        {
            "ticket_id": ["A", "B", "C"],
            "module": ["Accounting", "Fiscal", "Accounting"],
            "priority": ["Critical", "Low", "High"],
            "first_response_hours": [1.0, 3.0, 2.0],
            "resolution_hours": [5.0, 10.0, 15.0],
            "sla_met": [True, False, True],
        }
    )
    kpis = calculate_kpis(df)
    assert kpis["tickets"] == 3
    assert kpis["critical_tickets"] == 1
    assert kpis["avg_first_response_hours"] == 2.0
    assert kpis["avg_resolution_hours"] == 10.0
    assert kpis["sla_rate"] == pytest.approx(0.6667)

    by_module = tickets_by_module(df).set_index("module")
    assert by_module.loc["Accounting", "tickets"] == 2
    assert by_module.loc["Accounting", "sla_rate"] == 1.0
    assert by_module.loc["Fiscal", "sla_rate"] == 0.0


def test_metrics_work_on_filtered_subset() -> None:
    df = generate_tickets(n=300, seed=7)
    subset = df.loc[df["priority"] == "Critical"]
    if not subset.empty:
        assert calculate_kpis(subset)["tickets"] == len(subset)
        assert calculate_kpis(subset)["critical_tickets"] == len(subset)
