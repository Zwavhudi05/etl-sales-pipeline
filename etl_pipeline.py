"""
etl_pipeline.py
---------------
Main entry point. Orchestrates the full Extract → Transform → Load pipeline.

Usage:
    python etl_pipeline.py

Output:
    - warehouse.db          SQLite data warehouse (sales_fact table)
    - output/               Four summary CSV reports
    - logs/pipeline.log     Full run log with timestamps
"""

import pandas as pd
import logging
import os
import sys
import time
from datetime import datetime

import transform
import loader


# ─── Logging setup ───────────────────────────────────────────────────────────

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  [%(levelname)s]  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


# ─── Config ──────────────────────────────────────────────────────────────────

RAW_DATA_PATH = os.path.join("data", "superstore_raw.csv")


# ─── Extract ─────────────────────────────────────────────────────────────────

def extract(path: str) -> pd.DataFrame:
    """Load raw CSV from the data directory."""
    if not os.path.exists(path):
        logger.error(f"Source file not found: {path}")
        sys.exit(1)

    df = pd.read_csv(path)
    logger.info(f"Extracted {len(df):,} rows from {path}")
    return df


# ─── Pipeline runner ─────────────────────────────────────────────────────────

def run_pipeline():
    start_time = time.time()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    logger.info("=" * 60)
    logger.info(f"  SUPERSTORE ETL PIPELINE  |  Run ID: {run_id}")
    logger.info("=" * 60)

    # ── Extract
    logger.info("STEP 1: EXTRACT")
    raw_df = extract(RAW_DATA_PATH)

    # ── Transform
    logger.info("STEP 2: TRANSFORM")
    clean_df = transform.run_all(raw_df)

    # ── Load
    logger.info("STEP 3: LOAD")
    loader.load_to_warehouse(clean_df)
    loader.generate_summary_reports(clean_df)

    # ── Pipeline summary
    elapsed = round(time.time() - start_time, 2)
    logger.info("=" * 60)
    logger.info(f"  PIPELINE COMPLETE in {elapsed}s")
    logger.info(f"  Rows processed : {len(clean_df):,}")
    logger.info(f"  Warehouse      : warehouse.db → sales_fact")
    logger.info(f"  Reports        : output/")
    logger.info(f"  Log            : logs/pipeline.log")
    logger.info("=" * 60)


if __name__ == "__main__":
    run_pipeline()
