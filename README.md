# ERP Support Analytics Dashboard

Projeto funcional de analise de chamados de suporte ERP com dados sinteticos.

## Objetivo

Criar um fluxo simples para gerar tickets ficticios, calcular indicadores e preparar dados para dashboard.

## Funcionalidades

- Geracao de tickets sinteticos.
- Calculo de KPIs de suporte.
- Indicadores por modulo do sistema.
- Taxa de SLA.
- Tempo medio de primeira resposta.
- Tempo medio de resolucao.
- Base pronta para dashboard em Streamlit, Dash ou Power BI.

## Estrutura

```text
src/
  generate_tickets.py
  metrics.py

data/
  synthetic_erp_tickets.csv

reports/
  kpi_summary.csv
  module_summary.csv
```

## Como executar

```bash
pip install -r requirements.txt
python src/generate_tickets.py --rows 500 --output data/synthetic_erp_tickets.csv
```

Depois, use as funcoes de `src/metrics.py` em um notebook ou script para calcular os indicadores.

## Exemplo de uso em Python

```python
import pandas as pd
from src.metrics import calculate_kpis, tickets_by_module

df = pd.read_csv('data/synthetic_erp_tickets.csv')
print(calculate_kpis(df))
print(tickets_by_module(df))
```

## Indicadores calculados

- Total de tickets.
- Tempo medio de primeira resposta.
- Tempo medio de resolucao.
- Percentual de SLA cumprido.
- Total de tickets criticos.
- Tickets e SLA por modulo.

## Dados

A base e totalmente ficticia. Ela nao representa empresa, cliente, contrato ou sistema real.

## Proxima etapa

Criar `app/dashboard.py` para visualizar os indicadores em Streamlit ou Dash.

## Licenca

MIT License.
