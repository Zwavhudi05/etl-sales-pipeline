
import sqlite3
import pandas as pd


def load_sales_data():
    csv_path = "data/processed/sales_clean.csv"
    database_path = "data/sales.db"

    # Read transformed data
    df = pd.read_csv(csv_path)

    # Connect to SQLite database
    conn = sqlite3.connect(database_path)

    # Remove existing table for a full refresh
    conn.execute("DROP TABLE IF EXISTS sales")

    # Create sales table with explicit schema
    conn.execute("""
        CREATE TABLE sales (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT,
            customer_name TEXT,
            order_date TEXT,
            ship_date TEXT,
            region TEXT,
            category TEXT,
            sub_category TEXT,
            product_name TEXT,
            quantity INTEGER,
            sales REAL,
            discount REAL,
            profit REAL
        )
    """)

    # Load transformed data into SQLite
    df.to_sql(
        "sales",
        conn,
        if_exists="append",
        index=False
    )

    # Validate number of rows loaded
    loaded_rows = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    conn.close()

    return loaded_rows


if __name__ == "__main__":
    loaded_rows = load_sales_data()
    print(f"Rows loaded: {loaded_rows}")
