# IRCTC UTS Ticketing & Passenger Flow Analysis

A full-stack data analytics pipeline analyzing 89,000+ unreserved railway ticketing records. The project evaluates peak commuter travel windows, line-level revenue performance, and booking channel adoption using Python, Pandas, and MySQL.

## Project Structure
```text
IRCTC-Data-Analysis/
│
├── data/
│   ├── Uts_Data.csv              # Raw UTS passenger records
│   └── cleaned_uts_data.csv      # Cleaned and feature-engineered dataset
│
├── notebooks/
│   └── analysis.ipynb            # Interactive exploratory data analysis & KPIs
│
├── sql/
│   ├── database.sql              # MySQL DDL table schema
│   └── analysis.sql              # Aggregation & business analytical queries
│
├── src/
│   ├── data_cleaning.py          # Deduplication, temporal extraction, normalization
│   ├── database.py               # Batch database ingestion pipeline
│   └── data_analysis.py          # Production plotting & visual generation
│
├── visualizations/               # Output charts (peak hours, routes, modes)
├── requirements.txt              # Environment dependencies
└── README.md