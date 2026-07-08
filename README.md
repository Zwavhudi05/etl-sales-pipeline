Markdown
# Superstore Sales ETL Pipeline

A modular Python ETL pipeline that processes raw retail sales data through a full Extract → Transform → Load workflow — simulating how production data engineering teams move data cleanly from source systems into a structured queryable data warehouse.

The entire pipeline runs with a single command and completes in under one second.

---

## 🏗️ Pipeline Architecture

data/superstore_raw.csv
│
▼
┌───────────────────┐
│   EXTRACT         │  Read raw CSV into memory with robust quoting controls
└────────┬──────────┘
│
▼
┌───────────────────┐
│   TRANSFORM       │  Clean → Validate → Engineer Features
│                   │
│  • Standardise column names (lowercase + underscores)
│  • Parse date strings using localized formatting logic (DD/MM/YYYY)
│  • Drop invalid/corrupt records with missing critical identifiers
│  • Remove trailing formatting anomalies (rstrip semicolons from Sales)
│  • Engineer: order_year, order_month, order_quarter,
│              shipping_days, sales_band, is_high_value
└────────┬──────────┘
│
▼
┌───────────────────┐
│   LOAD            │  Write to SQLite Warehouse + Aggregated CSV Reports
└───────────────────┘
│
├── warehouse.db         → sales_fact table (7,353 rows, 24 columns)
├── output/revenue_by_category.csv
├── output/revenue_by_region.csv
├── output/monthly_revenue_trend.csv
└── output/top_customers.csv


---

## 🚀 Key Pipeline Features

📦 1. Extract
Reads `superstore_raw.csv` dynamically from the local directory. Validates the raw file exists before starting computation and utilizes explicit quoting rules parameters to manage mixed text fields cleanly.

⚙️ 2. Transform
Multi-stage data cleaning operations run sequentially, isolated inside modular functions within `transform.py`:
* **Column Standardization:** Converts headers to clean lowercase and snake_case formatting.
* **Localized Date Parsing:** Safely processes international string formats (DD/MM/YYYY) avoiding silent data conversion dropping.
* **Record Validation:** Automatically isolates and drops rows with unparseable data or null critical tracking IDs to protect down-stream transactional integrity.
* **String Massage:** Safely cleans trailing system punctuation (like trailing semicolons in financial values) to secure exact data type casting.
* **Feature Engineering:** Computes and appends 6 derived analytical columns on the fly for immediate analytics consumption.

💾 3. Load & Reporting
Persists the final 7,353 cleaned rows into a relational SQLite database (`warehouse.db`) table using a full-refresh pattern. The pipeline isolates database transactions inside strict `try-except-finally` blocks to completely eliminate thread locking and resource leaks. Concurrently, it compiles and exports 4 analytical views for executive tracking.

📊 4. Telemetry Logging
Every step writes runtime logs featuring precise timestamps to both standard out and a rolling, persistent file log tracker (`logs/pipeline.log`) for execution audatibility.

---

## 📂 Project Structure

```text
etl-sales-pipeline/
├── etl_pipeline.py          # Main orchestrator — project entry point
├── transform.py             # Data transformation and cleaning logic
├── loader.py                # Database connection and reporting logic
├── requirements.txt         # Project package dependencies
├── data/
│   └── superstore_raw.csv   # Raw input transactional records
├── output/                  # Generated dynamically on execution
│   ├── monthly_revenue_trend.csv
│   ├── revenue_by_category.csv
│   ├── revenue_by_region.csv
│   └── top_customers.csv
├── logs/                    # Generated dynamically on execution
│   └── pipeline.log
└── warehouse.db             # SQLite Relational Warehouse (generated on run)
🛠️ How to Run
1. Clone the repository
Bash
git clone [https://github.com/Zwavhudi05/etl-sales-pipeline.git](https://github.com/Zwavhudi05/etl-sales-pipeline.git)
cd etl-sales-pipeline
2. Install dependencies
Bash
pip install -r requirements.txt
3. Execute the pipeline
Bash
python etl_pipeline.py
Sample Execution Log Output
Plaintext
============================================================
  SUPERSTORE ETL PIPELINE  |  Run ID: 20260708_225504
============================================================
2026-07-08 22:55:04  [INFO]  STEP 1: EXTRACT
2026-07-08 22:55:04  [INFO]  Extracted 9,800 rows from data\superstore_raw.csv
2026-07-08 22:55:04  [INFO]  STEP 2: TRANSFORM
2026-07-08 22:55:04  [INFO]  --- Starting transformation chain ---
2026-07-08 22:55:04  [INFO]  Initial rows: 9800
2026-07-08 22:55:04  [INFO]  Columns standardised
2026-07-08 22:55:04  [INFO]  Dropped 2447 rows with missing critical data | 7353 rows remaining
2026-07-08 22:55:04  [INFO]  Feature engineering complete: 6 derived attributes built
2026-07-08 22:55:04  [INFO]  --- Transformation complete | Final shape: (7353, 24) ---
2026-07-08 22:55:04  [INFO]  STEP 3: LOAD
2026-07-08 22:55:05  [INFO]  Loaded 7,353 rows into 'sales_fact' table in warehouse.db
2026-07-08 22:55:05  [INFO]  All summary reports generated successfully.
============================================================
  PIPELINE COMPLETE in 0.53s
============================================================
Tech Stack
Python 3 - Operational Orchestration Engine

Pandas - Structural Matrix Extraction and Vector Transform

SQLite - Relational Data Storage Engine

Logging - Execution Telemetry Monitoring
