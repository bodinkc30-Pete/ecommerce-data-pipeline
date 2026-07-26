from pathlib import Path

import pandas as pd


SHOP_DATA_DIR = Path("data/raw/shop")

shop_files = sorted(SHOP_DATA_DIR.glob("*.xlsx"))
selected_files = [
    file_path
    for file_path in shop_files
    if not file_path.name.endswith("-4.xlsx")
]
print(f"Found {len(shop_files)} shop files")
print(f"Selected {len(selected_files)} files for processing")
reference_columns = None
dataframes = []
for file_path in selected_files:
    dataframe = pd.read_excel(
        file_path,
        sheet_name="Sheet1",
        engine="openpyxl",
        header=8,
    )
    dataframe["source_file"] = file_path.name
    dataframes.append(dataframe)
    current_columns = dataframe.columns.tolist()

    if reference_columns is None:
        reference_columns = current_columns

    same_schema = current_columns == reference_columns

    print(
        f"{file_path.name}: "
        f"{dataframe.shape[0]} rows, "
        f"{dataframe.shape[1]} columns, "
        f"same schema = {same_schema}"
    )
print(f"Stored {len(dataframes)} dataframes")
combined_dataframe = pd.concat(dataframes, ignore_index=True)
print(f"Combined rows: {combined_dataframe.shape[0]}")
print(f"First column: {combined_dataframe.columns[0]}")
duplicate_dates = combined_dataframe.duplicated(
    subset=[combined_dataframe.columns[0]]
).sum()
print(f"Duplicate dates: {duplicate_dates}")
print(f"Total columns after adding source_file: {combined_dataframe.shape[1]}")
print(f"Date column type: {combined_dataframe.iloc[:, 0].dtype}")
date_column = combined_dataframe.columns[0]

combined_dataframe[date_column] = pd.to_datetime(
    combined_dataframe[date_column],
    dayfirst=True,
    errors="coerce",
)
print(f"Date column type after conversion: {combined_dataframe.iloc[:, 0].dtype}")
invalid_dates = combined_dataframe[date_column].isna().sum()
print(f"Invalid dates: {invalid_dates}")
combined_dataframe = combined_dataframe.sort_values(
    by=date_column
).reset_index(drop=True)
print(f"First date: {combined_dataframe[date_column].min()}")
print(f"Last date: {combined_dataframe[date_column].max()}")

total_missing_values = combined_dataframe.isna().sum().sum()
print(f"Total missing values: {total_missing_values}")
numeric_dataframe = combined_dataframe.select_dtypes(include="number")
negative_values = (numeric_dataframe < 0).sum().sum()
print(f"Negative values: {negative_values}")
print(f"Numeric columns: {numeric_dataframe.shape[1]}")
print(combined_dataframe.dtypes)
print(combined_dataframe["รายได้รวม"].head(10))
print(combined_dataframe["รายได้รวม"].apply(type).value_counts())
text_revenue_values = combined_dataframe.loc[
    combined_dataframe["รายได้รวม"].apply(type) == str,
    "รายได้รวม",
]
print(text_revenue_values)
combined_dataframe["รายได้รวม"] = pd.to_numeric(
    combined_dataframe["รายได้รวม"],
    errors="coerce",
)
print(f"Revenue type after conversion: {combined_dataframe['รายได้รวม'].dtype}")
invalid_revenue = combined_dataframe["รายได้รวม"].isna().sum()
print(f"Invalid revenue values: {invalid_revenue}")
combined_dataframe["รายได้รวม"] = combined_dataframe["รายได้รวม"].fillna(0)
remaining_invalid_revenue = combined_dataframe["รายได้รวม"].isna().sum()
print(f"Remaining invalid revenue values: {remaining_invalid_revenue}")
print(combined_dataframe["รายได้รวม"].tail())
standard_columns = [
    "date",
    "gmv",
    "orders",
    "customers",
    "items_sold",
    "refunded_items",
    "sku_orders",
    "total_revenue",
    "page_views",
    "visitors",
    "conversion_rate",
    "product_impressions",
    "unique_product_impressions",
    "product_clicks",
    "unique_product_clicks",
    "aov",
    "live_gmv_creator",
    "live_gmv_creator_direct",
    "live_gmv_creator_indirect",
    "live_gmv_linked_account",
    "live_gmv_seller",
    "live_gmv_seller_indirect",
    "video_gmv_affiliate",
    "video_gmv_creator",
    "video_gmv_creator_indirect",
    "video_gmv_linked_account",
    "video_gmv_seller",
    "video_gmv_seller_indirect",
    "source_file",
]

if len(combined_dataframe.columns) != len(standard_columns):
    raise ValueError("Column count does not match the standard schema")
combined_dataframe.columns = standard_columns
print(combined_dataframe.columns.tolist())
OUTPUT_FILE = Path("data/staging/shop_daily.csv")
combined_dataframe.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)
print(f"Saved file: {OUTPUT_FILE}")
saved_dataframe = pd.read_csv(OUTPUT_FILE)
print(f"Saved CSV rows: {saved_dataframe.shape[0]}")
print(f"Saved CSV columns: {saved_dataframe.shape[1]}")
print(saved_dataframe.columns.tolist())
PROCESSED_FILE = Path("data/processed/shop_daily.csv")
combined_dataframe.to_csv(
    PROCESSED_FILE,
    index=False,
    encoding="utf-8-sig",
)
print(f"Saved processed file: {PROCESSED_FILE}")
