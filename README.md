# Retail Sales ETL Pipeline

A Python ETL project I built to practise moving raw sales data through a complete data pipeline — from extracting a CSV file to validating records and loading clean data into a SQLite database.

The main focus was data quality. Instead of silently removing invalid records, the pipeline separates them into a rejection file so they can be reviewed.

## What the Pipeline Does

1. **Extract:** Reads the raw sales data from a CSV file.
2. **Transform:** Validates records, handles invalid values, standardises selected fields, and separates rejected records.
3. **Load:** Stores the clean records in a SQLite database.
4. **Validate:** Checks row counts to make sure records are accounted for and the database load matches the clean dataset.
5. **Log:** Records pipeline progress, validation results, warnings, and errors.

## Tools Used

* Python
* pandas
* SQLite
* SQL
* Python logging
* Git and GitHub

## Project Structure

```text
retail-sales-etl/
├── config.py
├── run_pipeline.py
├── requirements.txt
├── data/
│   └── raw/
│       └── sales.csv
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── sql/
│   └── analysis.sql
└── .gitignore
```

Generated files, including cleaned data, rejected records, the SQLite database, and logs, are created when the pipeline runs.

## Data Quality Checks

The transformation stage applies the following rules:

* Reject records with missing order or customer IDs.
* Identify missing or invalid order and shipping dates.
* Reject records where the shipping date is earlier than the order date.
* Reject missing, invalid, or negative sales values.
* Reject missing or non-positive quantities.
* Standardise whitespace in region names and capitalisation in category names.
* Reject duplicate records.

Rejected rows are saved separately with a reason explaining why they failed validation.

## Latest Test Results

The latest successful local run processed 10,015 source records.

| Result           |   Rows |
| ---------------- | -----: |
| Source records   | 10,015 |
| Clean records    |  9,875 |
| Rejected records |    140 |

The pipeline checks that:

`Source rows = Clean rows + Rejected rows`

For this run, \(10,015 = 9,875 + 140\).

It also checks that the number of records loaded into SQLite matches the number of clean records.

## Database and SQL

The pipeline creates a SQLite database with a `sales` table and an explicit schema. The `order_id` column is defined as the primary key to prevent duplicate order IDs from being stored.

The file `sql/analysis.sql` contains SQL queries for exploring sales performance, including revenue, profit, regional performance, product performance, customer sales, and monthly trends.

## How to Run It

### 1. Install the dependencies

Python must be installed. Open a terminal in the project directory and run:

```bash
python -m pip install -r requirements.txt
```

### 2. Run the pipeline

```bash
python run_pipeline.py
```

The pipeline reads the raw CSV, transforms and validates the records, saves the clean and rejected datasets, loads the clean data into SQLite, and records execution details in the log.

## Generated Outputs

After running the pipeline, you should find:

* `data/processed/sales_clean.csv` — records that passed validation.
* `data/rejected/sales_rejected.csv` — rejected records and their reasons.
* `data/sales.db` — SQLite database containing the `sales` table.
* `logs/pipeline.log` — pipeline execution log.

These generated files are kept out of Git using `.gitignore`; the raw CSV and source code are included so the project can be run again.

## What I Want to Improve Next

* Add automated tests for transformation rules and edge cases.
* Introduce incremental loading instead of rebuilding the table on every run.
* Add more detailed data-quality metrics.
* Containerise the pipeline with Docker.
* Extend the database layer to PostgreSQL.

## Author

**Zwavhudi**

This project is part of my data engineering portfolio, where I'm building practical experience with Python, SQL, data quality, and database loading.


