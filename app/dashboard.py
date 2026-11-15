"""Interactive portfolio dashboard for fictional ERP support tickets.

All records are synthetic. No customer or company data is used.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.generate_tickets import generate_tickets  # noqa: E402
from src.metrics import calculate_kpis, tickets_by_module  # noqa: E402

DATA_PATH = ROOT / "data" / "synthetic_erp_tickets.csv"
REQUIRED_COLUMNS = {
    "ticket_id",
    "created_at",
    "module",
    "priority",
    "first_response_hours",
    "resolution_hours",
    "sla_met",
}


@st.cache_data(show_spinner=False)
def load_tickets() -> pd.DataFrame:
    """Read a local synthetic CSV or generate deterministic demo data."""
    df = pd.read_csv(DATA_PATH) if DATA_PATH.exists() else generate_tickets(n=500, seed=42)
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas ausentes no arquivo: {', '.join(sorted(missing))}")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df = df.dropna(subset=["created_at"]).copy()
    df["sla_met"] = df["sla_met"].astype(str).str.lower().eq("true")
    for col in ("first_response_hours", "resolution_hours"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["first_response_hours", "resolution_hours"])
    return df


st.set_page_config(page_title="ERP Support Analytics", page_icon="📊", layout="wide")
st.title("ERP Support Analytics")
st.caption(
    "Portfólio demonstrativo | chamados e resultados 100% sintéticos, "
    "sem associação a empresas, contratos ou clientes reais."
)

try:
    tickets = load_tickets()
except (OSError, ValueError, pd.errors.ParserError) as exc:
    st.error(f"Não foi possível carregar a base demonstrativa: {exc}")
    st.stop()

if tickets.empty:
    st.warning("A base demonstrativa não contém registros válidos.")
    st.stop()

min_date = tickets["created_at"].min().date()
max_date = tickets["created_at"].max().date()

with st.sidebar:
    st.header("Filtros")
    modules = st.multiselect(
        "Módulos do ERP",
        options=sorted(tickets["module"].dropna().unique()),
        default=sorted(tickets["module"].dropna().unique()),
    )
    priorities = st.multiselect(
        "Prioridades",
        options=sorted(tickets["priority"].dropna().unique()),
        default=sorted(tickets["priority"].dropna().unique()),
    )
    period = st.date_input(
        "Período de abertura",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

if not isinstance(period, (tuple, list)) or len(period) != 2:
    st.info("Selecione a data inicial e final para aplicar o filtro de período.")
    st.stop()

start_date, end_date = period
filtered = tickets.loc[
    tickets["module"].isin(modules)
    & tickets["priority"].isin(priorities)
    & tickets["created_at"].dt.date.between(start_date, end_date)
].copy()

if filtered.empty:
    st.warning("Nenhum chamado corresponde aos filtros selecionados.")
    st.stop()

kpis = calculate_kpis(filtered)
a, b, c, d, e = st.columns(5)
a.metric("Chamados", f'{kpis["tickets"]:,}'.replace(",", "."))
b.metric("SLA cumprido", f'{kpis["sla_rate"]:.1%}')
c.metric("1ª resposta (h)", f'{kpis["avg_first_response_hours"]:.2f}')
d.metric("Resolução (h)", f'{kpis["avg_resolution_hours"]:.2f}')
e.metric("Críticos", kpis["critical_tickets"])

left, right = st.columns(2)
with left:
    by_module = tickets_by_module(filtered)
    fig_module = px.bar(
        by_module,
        x="module",
        y="tickets",
        title="Chamados por módulo",
        labels={"module": "Módulo", "tickets": "Chamados"},
        text="tickets",
    )
    st.plotly_chart(fig_module, use_container_width=True)
with right:
    by_day = (
        filtered.assign(day=filtered["created_at"].dt.date)
        .groupby("day", as_index=False)
        .size()
        .rename(columns={"size": "tickets"})
    )
    fig_day = px.line(
        by_day,
        x="day",
        y="tickets",
        markers=True,
        title="Volume de chamados por dia",
        labels={"day": "Dia", "tickets": "Chamados"},
    )
    st.plotly_chart(fig_day, use_container_width=True)

st.subheader("SLA e tempo de resolução por módulo")
summary = tickets_by_module(filtered).rename(
    columns={
        "module": "Módulo",
        "tickets": "Chamados",
        "avg_resolution_hours": "Resolução média (h)",
    }
)
summary["SLA (%)"] = (summary.pop("sla_rate") * 100).round(1)
st.dataframe(summary, use_container_width=True, hide_index=True)
st.caption("Indicadores ilustrativos, calculados apenas com dados sintéticos.")

st.subheader("Registros filtrados")
st.dataframe(filtered.sort_values("created_at", ascending=False), use_container_width=True)
st.download_button(
    "Baixar CSV dos registros filtrados",
    data=filtered.to_csv(index=False).encode("utf-8-sig"),
    file_name="erp_tickets_filtrados.csv",
    mime="text/csv",
)

st.info(
    "Caso de estudo: priorize módulos com alto volume, baixa taxa de SLA "
    "e maior tempo de resolução. Os indicadores ilustram decisões possíveis; "
    "não demonstram desempenho real de qualquer organização."
)
