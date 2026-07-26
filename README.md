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

## Pipeline Architecture

```mermaid
flowchart LR
    A[Excel Source Files] --> B[Extract and Inspect]
    B --> C[Transform and Clean]
    C --> D[Processed CSV]
    D --> E[Load into SQLite]
    E --> F[SQL Analytics]
    F --> G[Business Insights]
```

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

## Sample Results

The processed dataset contains 105 daily records.

```text
Total GMV: 869,346.31
Total orders: 2,490
Average daily GMV: 8,279.49
Average GMV per order: 349.14

Highest GMV date: 2026-05-29
Highest GMV: 18,850.04

Highest orders date: 2026-04-30
Highest orders: 63
```

### Monthly Summary

| Month | Total GMV | Total Orders |
|---|---:|---:|
| 2026-04 | 221,224.21 | 670 |
| 2026-05 | 269,138.34 | 795 |
| 2026-06 | 267,751.02 | 708 |
| 2026-07 | 111,232.74 | 317 |

May 2026 generated the highest monthly GMV and the highest number of orders in the dataset.

## Challenges

### Inconsistent source schemas

The source Excel files contained column names in different formats. Some columns also contained extra spaces and inconsistent naming conventions.

The pipeline solved this by:

- inspecting source schemas before transformation
- standardizing column names
- mapping Thai column names to consistent English names
- validating the final schema before loading

### Mixed data types

Some numeric columns contained text values, causing Pandas to treat them as objects instead of numeric fields.

The pipeline solved this by:

- converting numeric columns with `pd.to_numeric`
- replacing invalid values with missing values
- validating the number of invalid records
- filling or correcting invalid values before export

### Missing revenue values

The revenue column contained an invalid value that could not be converted directly to a number.

The pipeline detected the invalid record, converted it to a missing value, and replaced it with `0.00` before loading the data into SQLite.

## Lessons Learned

Through this project, I learned how to:

- organize a data pipeline into Extract, Transform, Load, and Analytics stages
- inspect and validate Excel source files before processing
- clean inconsistent column names and data types with Pandas
- separate transformation, loading, and analytics responsibilities
- load processed data into SQLite
- write SQL queries for daily and monthly business analysis
- automate multiple pipeline stages with Python
- use Git and GitHub to version and publish a data engineering project
- protect private and generated data with `.gitignore`

## Installation

Clone the repository:

```bash
git clone https://github.com/bodinkc30-Pete/ecommerce-data-pipeline.git
```

Move into the project directory:

```bash
cd ecommerce-data-pipeline
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

## Run the Pipeline

Run the complete pipeline with one command:

```bash
python run_pipeline.py
```

The command runs the following stages:

```text
Transform → Load → Analytics
```

