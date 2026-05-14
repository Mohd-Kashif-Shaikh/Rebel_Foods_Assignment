# Cloud Kitchen PNL Dashboard

## Overview
Interactive Streamlit dashboard for analyzing cloud kitchen profitability, operational efficiency, and variance trends across stores and cities.

## Features
- Kitchen-level PNL analysis
- Variance analysis dashboard
- Interactive filters
- KPI cards
- Revenue and EBITDA trend analysis
- City and store performance insights
- Heatmap visualizations
- Download filtered data feature
- Dark theme UI

## Tech Stack
- Python
- Streamlit
- Plotly
- Pandas
- NumPy
- Statsmodels

## Project Structure
```text
Rebel_Food_Assignment/
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── kitchen.csv
│   └── processed_kitchen_pnl.csv
│
├── app.py
├── analysis.ipynb
├── requirements.txt
└── README.md
```

## Dashboard Modules
1. Kitchen Level PNL Dashboard
2. Variance Analysis Dashboard

## Run Locally

```bash
streamlit run app.py
```
