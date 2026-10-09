from src.extract import extract_sales_data
from src.transform import transform_sales_data
from src.load import load_sales_data

from config import (
    RAW_SALES_FILE,
    CLEAN_SALES_FILE,
    REJECTED_SALES_FILE,
    LOG_DIR,
    LOG_FILE
)

import logging


# Ensure the logs directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging to both file and console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_pipeline():
    try:
        logger.info("Pipeline started")

        # 1. EXTRACT
        df = extract_sales_data(RAW_SALES_FILE)
        logger.info(
            f"Extract complete: {len(df)} rows"
        )

        # 2. TRANSFORM
        transformed_df, rejected_df = transform_sales_data(df)

        # Save clean records
        transformed_df.to_csv(
            CLEAN_SALES_FILE,
            index=False
        )

        # Save rejected records
        rejected_df.to_csv(
            REJECTED_SALES_FILE,
            index=False
        )

        logger.info(
            f"Transform complete: "
            f"{len(transformed_df)} clean / "
            f"{len(rejected_df)} rejected"
        )

        # 3. ROW COUNT RECONCILIATION
        expected_rows = len(transformed_df) + len(rejected_df)

        if len(df) != expected_rows:
            raise ValueError(
                f"Row count reconciliation failed: "
                f"{len(df)} source rows != "
                f"{expected_rows} clean + rejected rows"
            )

        logger.info(
            f"Row count reconciliation passed: "
            f"{len(df)} source = "
            f"{len(transformed_df)} clean + "
            f"{len(rejected_df)} rejected"
        )

        if len(rejected_df) > 0:
            logger.warning(
                f"{len(rejected_df)} rows were rejected during transformation"
            )

        # 4. LOAD
        loaded_rows = load_sales_data()

        # 5. DATABASE LOAD VALIDATION
        if loaded_rows != len(transformed_df):
            raise ValueError(
                f"Load validation failed: "
                f"{len(transformed_df)} rows expected, "
                f"but {loaded_rows} rows found in database"
            )

        logger.info(
            f"Load validation passed: "
            f"{loaded_rows} rows loaded into database"
        )

        logger.info(
            "ETL pipeline completed successfully."
        )

    except Exception:
        logger.exception("ETL pipeline failed")
        raise


if __name__ == "__main__":
    run_pipeline()