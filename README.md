# Superstore ETL Pipeline

A modular Python ETL pipeline that processes raw retail sales data through a full Extract → Transform → Load workflow — simulating how data engineering teams move data from source systems into a queryable warehouse.

The entire pipeline runs with a single command and completes in under one second.

---

## Pipeline Architecture

```
data/superstore_raw.csv
        │
        ▼
┌───────────────────┐
│   EXTRACT         │  Read raw CSV into memory
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   TRANSFORM       │  Clean → Validate → Engineer features
│                   │
│  • Standardise column names
│  • Parse date strings to datetime
│  • Handle missing values (11 postal codes)
│  • Remove duplicates
│  • Validate sales values (drop zero/negative)
│  • Engineer: order_year, order_month, order_quarter,
│              shipping_days, sales_band, is_high_value
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   LOAD            │  Write to SQLite warehouse + CSV reports
└───────────────────┘
         │
         ├── warehouse.db         → sales_fact table (9,800 rows, 24 columns)
         ├── output/revenue_by_category.csv
         ├── output/revenue_by_region.csv
         ├── output/monthly_revenue_trend.csv
         ├── output/top_customers.csv
         └── logs/pipeline.log
```

---

## What the Pipeline Does

### Extract
Reads `superstore_raw.csv` from the `data/` directory. Validates the file exists before proceeding and exits with a clear error message if not found.

### Transform
Seven transformation steps run in sequence, each isolated in its own function inside `transform.py`:

| Step | Function | What it does |
|---|---|---|
| 1 | `standardise_columns` | Lowercase + underscore column names |
| 2 | `parse_dates` | Convert date strings to datetime |
| 3 | `handle_missing` | Fill postal code nulls; median for numerics |
| 4 | `remove_duplicates` | Drop fully duplicate rows |
| 5 | `validate_sales` | Remove zero and negative sales values |
| 6 | `engineer_features` | Add 6 derived analytical columns |

### Load
Writes the cleaned data to a SQLite database (`warehouse.db`) using a full-refresh pattern — the table is replaced on every run to ensure consistency. Four summary reports are also exported as CSVs for downstream analysis.

### Logging
Every step is logged with a timestamp to both the console and `logs/pipeline.log`. This means every pipeline run is fully auditable.

---

## Sample Log Output

```
2024-01-15 09:32:11  [INFO]  ============================================================
2024-01-15 09:32:11  [INFO]    SUPERSTORE ETL PIPELINE  |  Run ID: 20240115_093211
2024-01-15 09:32:11  [INFO]  ============================================================
2024-01-15 09:32:11  [INFO]  STEP 1: EXTRACT
2024-01-15 09:32:11  [INFO]  Extracted 9,800 rows from data/superstore_raw.csv
2024-01-15 09:32:11  [INFO]  STEP 2: TRANSFORM
2024-01-15 09:32:11  [INFO]  Missing values: 11 before → 0 after handling.
2024-01-15 09:32:11  [INFO]  ─── Transformation complete | Final shape: (9800, 24) ───
2024-01-15 09:32:11  [INFO]  STEP 3: LOAD
2024-01-15 09:32:11  [INFO]  Loaded 9,800 rows into 'sales_fact' table in warehouse.db
2024-01-15 09:32:11  [INFO]  PIPELINE COMPLETE in 0.3s
```

---

## Project Structure

```
etl-sales-pipeline/
├── etl_pipeline.py          # Main orchestrator — run this
├── transform.py             # All cleaning and transformation logic
├── loader.py                # SQLite loader and report generator
├── data/
│   └── superstore_raw.csv   # Raw input data (Kaggle Superstore dataset)
├── output/                  # Generated on first run
│   ├── revenue_by_category.csv
│   ├── revenue_by_region.csv
│   ├── monthly_revenue_trend.csv
│   └── top_customers.csv
├── logs/                    # Generated on first run
│   └── pipeline.log
├── warehouse.db             # SQLite warehouse (generated on first run)
└── README.md
```

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/Zwavhudi05/etl-sales-pipeline.git
cd etl-sales-pipeline
```

**2. Install dependencies**
```bash
pip install pandas
```

**3. Run the pipeline**
```bash
python etl_pipeline.py
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| pandas | Data extraction and transformation |
| SQLite | Lightweight data warehouse |
| logging | Automated run logging |
| os / sys | File handling and error management |

---

## Dataset

Superstore retail sales data — 9,800 order records across 4 US regions, 3 product categories, and 3 customer segments. Source: [Kaggle Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final).

---

## Author

**Zwavhudi Mudogwa**  
Data Analytics | Cloud | IT Support  
📧 mudogwa.zwavhu@gmail.com  
🔗 [linkedin.com/in/zwavhudi-mudogwa5](https://www.linkedin.com/in/zwavhudi-mudogwa5)  
🗂️ [datascienceportfol.io/mudogwazwavhu](https://datascienceportfol.io/mudogwazwavhu)
