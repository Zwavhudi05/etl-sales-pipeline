from pathlib import Path
import pandas as pd
import logging

from config import RAW_SALES_FILE

logger = logging.getLogger(__name__)


def extract_sales_data(file_path=RAW_SALES_FILE):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Source file not found: {path}"
        )

    df = pd.read_csv(path)

    rows, columns = df.shape

    logger.info(f"Rows extracted: {rows}")
    logger.info(f"Columns extracted: {columns}")

    return df


if __name__ == "__main__":
    df = extract_sales_data()

    transformed_df, rejected_df = transform_sales_data(df)

    transformed_df.to_csv(
        CLEAN_SALES_FILE,
        index=False
    )

    rejected_df.to_csv(
        REJECTED_SALES_FILE,
        index=False
    )

    print(f"Rows before transformation: {len(df)}")
    print(f"Rows after transformation: {len(transformed_df)}")
    print(f"Total rejected rows: {len(rejected_df)}")