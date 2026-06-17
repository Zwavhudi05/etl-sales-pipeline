"""
transform.py
------------
All cleaning and transformation logic for the Superstore ETL pipeline.
Each function takes a DataFrame, applies one concern, and returns it.
"""

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names and replace spaces with underscores."""
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    logger.info(f"Columns standardised: {df.columns.tolist()}")
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert order_date and ship_date strings to datetime objects."""
    for col in ["order_date", "ship_date"]:
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
    unparsed = df["order_date"].isna().sum()
    if unparsed > 0:
        logger.warning(f"{unparsed} rows had unparseable order_date values.")
    logger.info("Date columns parsed to datetime.")
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values:
    - postal_code: fill with 0 (unknown) since it is not used in analysis
    - Any remaining numeric nulls: fill with column median
    - Any remaining string nulls: fill with 'Unknown'
    """
    before = df.isnull().sum().sum()

    df["postal_code"] = df["postal_code"].fillna(0).astype(int)

    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna("Unknown")

    after = df.isnull().sum().sum()
    logger.info(f"Missing values: {before} before → {after} after handling.")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop fully duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    logger.info(f"Duplicates removed: {removed} | Rows remaining: {len(df)}")
    return df


def validate_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag and remove rows where sales is zero or negative.
    These represent data entry errors or returns that skew analysis.
    """
    invalid = df[df["sales"] <= 0]
    if len(invalid) > 0:
        logger.warning(
            f"{len(invalid)} rows with sales <= 0 flagged and removed."
        )
    df = df[df["sales"] > 0].copy()
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived columns that add analytical value:
    - order_year, order_month, order_quarter
    - shipping_days (days between order and ship date)
    - sales_band (Low / Medium / High / Premium)
    - is_high_value (boolean flag for orders above $500)
    """
    df["order_year"]    = df["order_date"].dt.year
    df["order_month"]   = df["order_date"].dt.month
    df["order_quarter"] = df["order_date"].dt.quarter

    df["shipping_days"] = (
        df["ship_date"] - df["order_date"]
    ).dt.days

    df["sales_band"] = pd.cut(
        df["sales"],
        bins=[0, 50, 200, 500, float("inf")],
        labels=["Low", "Medium", "High", "Premium"]
    )

    df["is_high_value"] = df["sales"] > 500

    logger.info(
        "Feature engineering complete: "
        "order_year, order_month, order_quarter, "
        "shipping_days, sales_band, is_high_value"
    )
    return df


def run_all(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full transformation chain in order."""
    logger.info("─── Starting transformation chain ───")
    df = standardise_columns(df)
    df = parse_dates(df)
    df = handle_missing(df)
    df = remove_duplicates(df)
    df = validate_sales(df)
    df = engineer_features(df)
    logger.info(f"─── Transformation complete | Final shape: {df.shape} ───")
    return df
