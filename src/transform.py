import pandas as pd
from src.extract import extract_sales_data
import logging

logger = logging.getLogger(__name__)


def transform_sales_data(df):
    transformed_df = df.copy()

    # 1. Reject rows with missing IDs
    missing_id_mask = (
        transformed_df["order_id"].isna()
        | transformed_df["customer_id"].isna()
    )

    rejected_df = transformed_df[missing_id_mask].copy()
    rejected_df["reject_reason"] = "Missing order_id or customer_id"
    logger.warning(
    f"Rejected {len(rejected_df)} rows: missing order_id or customer_id"
    )
    transformed_df = transformed_df[~missing_id_mask].copy()

    # 2. Convert date columns
    transformed_df["order_date"] = pd.to_datetime(
        transformed_df["order_date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    transformed_df["ship_date"] = pd.to_datetime(
        transformed_df["ship_date"],
        format="%d/%m/%Y",
        errors="coerce"
    )

    # 3. Reject rows with invalid dates
    invalid_date_mask = (
        transformed_df["order_date"].isna()
        | transformed_df["ship_date"].isna()
    )

    invalid_date_rows = transformed_df[invalid_date_mask].copy()
    invalid_date_rows["reject_reason"] = "Invalid order_date or ship_date"
    
    logger.warning(
    f"Rejected {len(invalid_date_rows)} rows: invalid order_date or ship_date"
    )

    rejected_df = pd.concat(
        [rejected_df, invalid_date_rows],
        ignore_index=True
    )

    transformed_df = transformed_df[~invalid_date_mask].copy()

    # 4. Reject rows where ship_date is before order_date
    invalid_ship_date_mask = (
        transformed_df["ship_date"] < transformed_df["order_date"]
    )

    invalid_ship_date_rows = transformed_df[
        invalid_ship_date_mask
    ].copy()

    invalid_ship_date_rows["reject_reason"] = (
        "ship_date before order_date"
    )
    
    logger.warning(
    f"Rejected {len(invalid_ship_date_rows)} rows: ship_date before order_date"
    )

    rejected_df = pd.concat(
        [rejected_df, invalid_ship_date_rows],
        ignore_index=True
    )

    transformed_df = transformed_df[~invalid_ship_date_mask].copy()

    # 5. Convert sales to numeric
    transformed_df["sales"] = pd.to_numeric(
        transformed_df["sales"],
        errors="coerce"
    )

    # 6. Reject rows with invalid sales values
    invalid_sales_mask = (
        transformed_df["sales"].isna()
        | (transformed_df["sales"] < 0)
    )

    invalid_sales_rows = transformed_df[invalid_sales_mask].copy()
    invalid_sales_rows["reject_reason"] = "Invalid sales value"

    logger.warning(
    f"Rejected {len(invalid_sales_rows)} rows: invalid sales value"
    )
    rejected_df = pd.concat(
        [rejected_df, invalid_sales_rows],
        ignore_index=True
    )

    transformed_df = transformed_df[~invalid_sales_mask].copy()

    # 7. Reject rows with invalid quantity values
    invalid_quantity_mask = (
        transformed_df["quantity"].isna()
        | (transformed_df["quantity"] <= 0)
    )

    invalid_quantity_rows = transformed_df[
        invalid_quantity_mask
    ].copy()

    invalid_quantity_rows["reject_reason"] = "Invalid quantity value"

    rejected_df = pd.concat(
        [rejected_df, invalid_quantity_rows],
        ignore_index=True
    )

    transformed_df = transformed_df[~invalid_quantity_mask].copy()

    # 8. Reject exact duplicate records
    duplicate_mask = transformed_df.duplicated(keep="first")

    duplicate_rows = transformed_df[duplicate_mask].copy()
    duplicate_rows["reject_reason"] = "Duplicate record"

    logger.warning(
    f"Rejected {len(duplicate_rows)} rows: duplicate record"
    ) 
    
    rejected_df = pd.concat(
        [rejected_df, duplicate_rows],
        ignore_index=True
    )
    
    # 9. Standardize category capitalization
    transformed_df["category"] = transformed_df["category"].str.title()
    
    transformed_df["region"] = transformed_df["region"].str.strip()

    transformed_df = transformed_df[~duplicate_mask].copy()

    return transformed_df, rejected_df


if __name__ == "__main__":
    df = extract_sales_data("data/raw/sales.csv")

    transformed_df, rejected_df = transform_sales_data(df)
    
    transformed_df.to_csv(
        "data/processed/sales_clean.csv",
        index=False
    )
    
    rejected_df.to_csv(
        "data/rejected/sales_rejected.csv",
        index=False
    )

    print(f"Rows before transformation: {len(df)}")
    print(f"Rows after transformation: {len(transformed_df)}")
    print(f"Total rejected rows: {len(rejected_df)}")

    print("\nRejection reasons:")
    print(rejected_df["reject_reason"].value_counts())
    
    
    
    