from pathlib import Path
import sqlite3
import pandas as pd


INPUT_FILE = Path("data/processed/shop_daily.csv")
DATABASE_FILE = Path("data/processed/ecommerce.db")
TABLE_NAME = "shop_daily"


dataframe = pd.read_csv(INPUT_FILE)

with sqlite3.connect(DATABASE_FILE) as connection:
    dataframe.to_sql(
        TABLE_NAME,
        connection,
        if_exists="replace",
        index=False,
    )

    row_count = connection.execute(
        f"SELECT COUNT(*) FROM {TABLE_NAME}"
    ).fetchone()[0]


print(f"Loaded {row_count} rows into table: {TABLE_NAME}")
print(f"Database file: {DATABASE_FILE}")
