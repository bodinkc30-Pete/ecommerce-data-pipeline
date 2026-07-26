from pathlib import Path

import pandas as pd


SHOP_DATA_DIR = Path("data/raw/shop")

shop_files = sorted(SHOP_DATA_DIR.glob("*.xlsx"))

first_file = shop_files[0]

print(f"Reading file: {first_file}")

dataframe = pd.read_excel(
    first_file,
    sheet_name="Sheet1",
    engine="openpyxl",
    header=8,
)

print(f"Rows: {dataframe.shape[0]}")
print(f"Columns: {dataframe.shape[1]}")

print("\nColumn names:")

for column in dataframe.columns:
    print(column)

print("\nFirst 5 data rows:")
print(dataframe.head())