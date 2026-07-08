"""
loader.py
---------
Handles loading the transformed DataFrame into a SQLite data warehouse
and generating summary output CSVs for analysts.
"""

import sqlite3
import pandas as pd
import logging
import os

logger = logging.getLogger(__name__)

DB_PATH = "warehouse.db"


def load_to_warehouse(df: pd.DataFrame, table: str = "sales_fact") -> None:
    """
    Load the cleaned DataFrame into SQLite.
    Replaces the table on each run (full refresh pattern).
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        df.to_sql(table, conn, if_exists="replace", index=False)
        row_count = len(df)
        logger.info(
            f"Loaded {row_count:,} rows into '{table}' table in {DB_PATH}"
        )
    except Exception as e:
        logger.error(f"Failed to load data into warehouse: {e}")
        raise
    finally:
        if conn:
            conn.close()


def generate_summary_reports(df: pd.DataFrame, output_dir: str = "output") -> None:
    """
    Generate four summary CSV files from the cleaned data:
    1. Revenue by category
    2. Revenue by region
    3. Monthly revenue trend
    4. Top 20 customers by revenue
    """
    try:
        os.makedirs(output_dir, exist_ok=True)

        # Validate required columns exist
        required_cols = {"category", "region", "order_id", "sales", "order_year", "order_month", "customer_id", "customer_name", "segment"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns for reports: {missing_cols}")

        # 1. Revenue by category
        category_summary = (
            df.groupby("category")
            .agg(
                total_orders=("order_id", "count"),
                total_revenue=("sales", "sum"),
                avg_order_value=("sales", "mean")
            )
            .round(2)
            .reset_index()
            .sort_values("total_revenue", ascending=False)
        )
        path1 = os.path.join(output_dir, "revenue_by_category.csv")
        category_summary.to_csv(path1, index=False)
        logger.info(f"Summary saved: {path1}")

        # 2. Revenue by region
        region_summary = (
            df.groupby("region")
            .agg(
                total_orders=("order_id", "count"),
                total_revenue=("sales", "sum"),
                avg_order_value=("sales", "mean")
            )
            .round(2)
            .reset_index()
            .sort_values("total_revenue", ascending=False)
        )
        path2 = os.path.join(output_dir, "revenue_by_region.csv")
        region_summary.to_csv(path2, index=False)
        logger.info(f"Summary saved: {path2}")

        # 3. Monthly revenue trend
        monthly_trend = (
            df.groupby(["order_year", "order_month"])
            .agg(total_revenue=("sales", "sum"), total_orders=("order_id", "count"))
            .round(2)
            .reset_index()
            .sort_values(["order_year", "order_month"])
        )
        path3 = os.path.join(output_dir, "monthly_revenue_trend.csv")
        monthly_trend.to_csv(path3, index=False)
        logger.info(f"Summary saved: {path3}")

        # 4. Top 20 customers by lifetime value
        top_customers = (
            df.groupby(["customer_id", "customer_name", "segment"])
            .agg(
                total_orders=("order_id", "nunique"),
                lifetime_value=("sales", "sum")
            )
            .round(2)
            .reset_index()
            .sort_values("lifetime_value", ascending=False)
            .head(20)
        )
        path4 = os.path.join(output_dir, "top_customers.csv")
        top_customers.to_csv(path4, index=False)
        logger.info(f"Summary saved: {path4}")

        logger.info("All summary reports generated successfully.")
    except Exception as e:
        logger.error(f"Failed to generate summary reports: {e}")
        raise
