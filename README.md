# E-commerce Data Pipeline

Python ETL pipeline สำหรับรวม ทำความสะอาด โหลด และวิเคราะห์ข้อมูล E-commerce จากไฟล์ Excel หลายไฟล์

## Pipeline

1. Inspect Excel source files
2. Transform and clean the data
3. Validate dates, missing values, and numeric fields
4. Standardize column names
5. Export processed data to CSV
6. Load the processed data into SQLite
7. Analyze the data using SQL

## Technologies

- Python
- Pandas
- SQL
- SQLite
- OpenPyXL

## Project Structure

```text
ecommerce-data-pipeline/
├── data/
│   ├── raw/
│   ├── staging/
│   └── processed/
├── src/
│   ├── extract/
│   │   └── inspect_excel.py
│   ├── transform/
│   │   └── clean_shop.py
│   ├── load/
│   │   └── load_shop_sqlite.py
│   └── analytics/
│       └── analyze_shop.py
├── run_pipeline.py
├── requirements.txt
├── .gitignore
└── README.md