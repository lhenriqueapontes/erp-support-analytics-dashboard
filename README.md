# ERP Support Analytics Dashboard

**Portfólio demonstrativo de análise de suporte ERP em Python e Streamlit.** O projeto gera chamados **100% sintéticos** e permite explorar indicadores de atendimento, sem usar informações de empresas ou clientes reais.

> Status: dashboard implementado nesta branch de revisão. O sistema não está publicado como serviço e não representa uma implantação comercial.

## O que demonstra

- Geração reprodutível de chamados fictícios, com prioridades, módulos, categorias e tempos de atendimento.
- KPIs: volume, taxa de cumprimento do SLA, primeira resposta, resolução e chamados críticos.
- Dashboard interativo em **Streamlit** com filtros por módulo, prioridade e período.
- Gráficos de volume por módulo e evolução por dia, tabela comparativa de SLA e exportação CSV.
- Testes de regressão com **pytest** e verificação automatizada no GitHub Actions.

## Executar localmente

Pré-requisito: Python 3.11 ou superior.

```bash
git clone https://github.com/lhenriqueapontes/erp-support-analytics-dashboard.git
cd erp-support-analytics-dashboard
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python src/generate_tickets.py --rows 500 --output data/synthetic_erp_tickets.csv
python -m streamlit run app/dashboard.py
```

O Streamlit mostrará um endereço local no terminal (em geral `http://localhost:8501`). O painel também pode gerar dados demonstrativos automaticamente se o CSV não existir.

Para executar os testes:

```bash
python -m pip install pytest
python -m pytest -q
```

## Estrutura principal

```text
app/dashboard.py                    # painel interativo
src/generate_tickets.py            # gerador de dados sintéticos
src/metrics.py                     # cálculos de KPIs e agrupamentos
tests/test_metrics.py              # verificações automatizadas
.github/workflows/python-tests.yml # CI de testes em pull requests
requirements.txt
README.md
```

A pasta `data/` pode ser criada automaticamente ao gerar o CSV; não é necessário armazenar dados de clientes.

## Perguntas de negócio que a demo permite investigar

1. Qual módulo concentra mais solicitações?
2. Qual prioridade está mais associada a falhas de SLA?
3. Quais módulos têm maior tempo de resolução?
4. Como o volume de chamados varia no período selecionado?

As respostas são **simulações ilustrativas**; não autorizam conclusões sobre a operação de nenhuma empresa.

## Limitações e próximos passos

- Os dados são gerados artificialmente e as metas de SLA são simplificadas.
- O projeto não tem login, persistência em banco, integração com ERP real ou monitoramento em produção.
- Sugestões futuras: testes do fluxo completo do painel, exemplos visuais (screenshots), publicação opcional da demo, análises de tendências e documentação de decisões baseadas nos indicadores.
- Nenhuma melhoria de SLA, redução de custos ou ganho real de clientes foi medida.

## Ética, autoria e licença

Projeto de demonstração educacional e de portfólio, com dados fictícios. Não deve receber credenciais, documentos internos nem dados pessoais de pacientes ou clientes.

Licença MIT — consulte `LICENSE`.
