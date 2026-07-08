# Superstore Sales ETL Pipeline

A modular Python **Extract → Transform → Load (ETL)** pipeline that processes raw retail sales data into a clean SQLite data warehouse and automatically generates analytical reports.

The project simulates a real-world data engineering workflow by extracting raw transactional data, performing extensive cleaning and feature engineering, loading the processed data into a relational database, and exporting business-ready summary reports.

---

## Features

- Modular ETL architecture
- Automated data cleaning and validation
- Feature engineering for analytics
- SQLite data warehouse
- Automatic CSV report generation
- Comprehensive execution logging
- Runs with a single command
- Completes in under one second

---

# Pipeline Architecture

```text
data/superstore_raw.csv
        │
        ▼
┌──────────────────────────────┐
│          EXTRACT             │
│ Read raw CSV into memory     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         TRANSFORM            │
│                              │
│ • Standardise column names   │
│ • Parse dates                │
│ • Validate records           │
│ • Remove formatting issues   │
│ • Engineer new features      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│            LOAD              │
│ SQLite Warehouse             │
│ CSV Summary Reports          │
└──────────────────────────────┘
               │
               ├── warehouse.db
               ├── revenue_by_category.csv
               ├── revenue_by_region.csv
               ├── monthly_revenue_trend.csv
               └── top_customers.csv
```

---

# Project Structure

```text
etl-sales-pipeline/
│
├── etl_pipeline.py          # Main ETL orchestrator
├── transform.py             # Data cleaning & feature engineering
├── loader.py                # Database loading & report generation
├── requirements.txt
│
├── data/
│   └── superstore_raw.csv
│
├── output/
│   ├── monthly_revenue_trend.csv
│   ├── revenue_by_category.csv
│   ├── revenue_by_region.csv
│   └── top_customers.csv
│
├── logs/
│   └── pipeline.log
│
└── warehouse.db
```

---

# ⚙️ ETL Workflow

## 1️⃣ Extract

The pipeline:

- Reads the raw CSV dataset
- Validates the file exists
- Uses explicit CSV parsing options
- Loads the dataset into a Pandas DataFrame

---

## 2️⃣ Transform

The transformation stage performs multiple data quality operations.

### Column Standardisation

- Converts column names to lowercase
- Replaces spaces with underscores

Example:

```
Order Date
```

becomes

```
order_date
```

---

### Date Parsing

Safely converts localized date strings (`DD/MM/YYYY`) into proper datetime objects.

---

### Data Validation

Automatically removes records containing:

- Missing Order IDs
- Missing Customer IDs
- Invalid dates
- Corrupt records

---

### Data Cleaning

Removes formatting anomalies including:

- Trailing semicolons
- Incorrect numeric formatting
- Invalid data types

---

### Feature Engineering

Creates six analytical columns:

| Feature | Description |
|----------|-------------|
| order_year | Year of purchase |
| order_month | Month number |
| order_quarter | Quarter of sale |
| shipping_days | Delivery duration |
| sales_band | Sales category |
| is_high_value | High-value transaction flag |

---

## 3️⃣ Load

The cleaned dataset is loaded into a SQLite data warehouse using a full-refresh approach.

Database table:

```
sales_fact
```

The pipeline also exports four analytical reports:

- Revenue by Category
- Revenue by Region
- Monthly Revenue Trend
- Top Customers

---

## 📊 Output

After execution, the project generates:

```text
warehouse.db

output/
├── revenue_by_category.csv
├── revenue_by_region.csv
├── monthly_revenue_trend.csv
└── top_customers.csv
```

---

# 📝 Logging

Every ETL stage is logged with timestamps.

Example:

```text
2026-07-08 22:55:04 [INFO] STEP 1: EXTRACT
2026-07-08 22:55:04 [INFO] Extracted 9800 rows
2026-07-08 22:55:04 [INFO] STEP 2: TRANSFORM
2026-07-08 22:55:04 [INFO] Feature engineering complete
2026-07-08 22:55:05 [INFO] STEP 3: LOAD
2026-07-08 22:55:05 [INFO] Loaded 7353 rows into warehouse.db
2026-07-08 22:55:05 [INFO] Reports generated successfully
```

Logs are written to:

```
logs/pipeline.log
```

---

# ▶️ Getting Started

## Clone the repository

```bash
git clone https://github.com/Zwavhudi05/etl-sales-pipeline.git

cd etl-sales-pipeline
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the pipeline

```bash
python etl_pipeline.py
```

---

# 📈 Sample Run

```text
============================================================
SUPERSTORE ETL PIPELINE
Run ID: 20260708_225504
============================================================

STEP 1: EXTRACT
✓ Extracted 9,800 rows

STEP 2: TRANSFORM
✓ Standardised columns
✓ Removed invalid records
✓ Engineered 6 new features

STEP 3: LOAD
✓ Loaded 7,353 rows into SQLite
✓ Generated 4 analytical reports

============================================================
Pipeline completed in 0.53 seconds
============================================================
```

---

# 🛠️ Tech Stack

- Python 3
- Pandas
- SQLite
- Logging
- CSV
- Git
- GitHub

---

---

## 👨‍💻 Author

**Zwavhudi Mudogwa**

GitHub: https://github.com/Zwavhudi05
