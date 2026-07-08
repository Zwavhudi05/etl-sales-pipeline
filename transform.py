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
        .str.replace(";", "", regex=False)
    )
    logger.info(f"Columns standardised: {df.columns.tolist()}")
    return df


def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Convert order_date and ship_date strings to datetime objects."""
    for col in ["order_date", "ship_date"]:
        if col not in df.columns:
            logger.warning(f"Column '{col}' not found. Skipping date parsing.")
            continue
        df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
    unparsed = df["order_date"].isna().sum()
    if unparsed > 0:
        logger.warning(f"{unparsed} rows had unparseable order_date values. Consider checking date format.")
        if unparsed > len(df) * 0.1:
            logger.warning(f"WARNING: More than 10% of dates unparseable ({unparsed}/{len(df)})!")
    logger.info("Date columns parsed to datetime.")
    return df


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values:
    - Drop rows where critical date/order fields are null (these represent bad records)
    - postal_code: fill with 0 (unknown) since it is not used in analysis
    - Parse sales to numeric before filling
    - Any remaining numeric nulls: fill with column median
    - Any remaining string nulls: fill with 'Unknown'
    """
    before = len(df)

    # Drop rows where order_date or order_id is null (bad records)
    if "order_date" in df.columns:
        df = df.dropna(subset=["order_date"])
    if "order_id" in df.columns:
        df = df.dropna(subset=["order_id"])

    # Convert sales to numeric early
    if "sales" in df.columns and df["sales"].dtype == "object":
        df["sales"] = df["sales"].astype(str).str.rstrip(";").str.strip()
        df["sales"] = pd.to_numeric(df["sales"], errors="coerce")

    if "postal_code" in df.columns:
        df["postal_code"] = pd.to_numeric(df["postal_code"], errors="coerce").fillna(0).astype(int)

    # Fill numeric nulls with median
    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # Fill string nulls with 'Unknown'
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        if col not in ["order_date", "ship_date"]:  # Don't fill date columns
            if df[col].isnull().any():
                df[col] = df[col].fillna("Unknown")

    after = len(df)
    logger.info(f"Dropped {before - after} rows with missing critical data | {after} rows remaining")
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
    if "sales" not in df.columns:
        logger.warning("'sales' column not found. Skipping sales validation.")
        return df
    
    # Ensure sales is numeric
    if not pd.api.types.is_numeric_dtype(df["sales"]):
        df["sales"] = df["sales"].astype(str).str.rstrip(";").str.strip()
        df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    
    # Drop rows with missing or invalid sales
    before = len(df)
    df = df.dropna(subset=["sales"])
    df = df[df["sales"] > 0].copy()
    removed = before - len(df)
    
    if removed > 0:
        logger.warning(f"{removed} rows with invalid, zero, or negative sales removed.")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create derived columns that add analytical value:
    - order_year, order_month, order_quarter
    - shipping_days (days between order and ship date)
    - sales_band (Low / Medium / High / Premium)
    - is_high_value (boolean flag for orders above $500)
    """
    # Validate required columns
    required = {"order_date", "ship_date", "sales"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns for feature engineering: {missing}")

    # Ensure datetime types
    if df["order_date"].dtype == "object":
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    if df["ship_date"].dtype == "object":
        df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")

    # Only extract date parts from valid (non-NaT) dates
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

    # Log info about invalid dates
    invalid_dates = df["order_year"].isna().sum()
    if invalid_dates > 0:
        logger.warning(f"{invalid_dates} rows with invalid order_date (removed from analysis)")

    logger.info(
        "Feature engineering complete: "
        "order_year, order_month, order_quarter, "
        "shipping_days, sales_band, is_high_value"
    )
    return df


def run_all(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full transformation chain in order."""
    logger.info("--- Starting transformation chain ---")
    logger.info(f"Initial rows: {len(df)}")
    
    df = standardise_columns(df)
    df = parse_dates(df)
    logger.info(f"After parse_dates: {len(df)} rows")
    
    df = handle_missing(df)
    logger.info(f"After handle_missing: {len(df)} rows")
    
    df = remove_duplicates(df)
    logger.info(f"After remove_duplicates: {len(df)} rows")
    
    df = validate_sales(df)
    logger.info(f"After validate_sales: {len(df)} rows")
    
    df = engineer_features(df)
    logger.info(f"After engineer_features: {len(df)} rows")
    
    logger.info(f"--- Transformation complete | Final shape: {df.shape} ---")
    return df
