import csv
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATABASE_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ecommerce.db"
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "portfolio_outputs"
)


EXPORT_QUERIES = {
    "sample_daily_performance.csv": """
        SELECT
            date,
            ROUND(gmv, 2) AS gmv,
            orders,
            customers,
            items_sold,
            ROUND(total_revenue, 2) AS total_revenue,
            page_views,
            visitors,
            ROUND(conversion_rate, 4)
                AS conversion_rate,
            ROUND(aov, 2)
                AS average_order_value
        FROM shop_daily
        ORDER BY date
        LIMIT 30;
    """,

    "sample_top_revenue_days.csv": """
        SELECT
            date,
            ROUND(total_revenue, 2)
                AS total_revenue,
            ROUND(gmv, 2)
                AS gmv,
            orders,
            customers,
            ROUND(aov, 2)
                AS average_order_value,
            ROUND(conversion_rate, 4)
                AS conversion_rate
        FROM shop_daily
        WHERE total_revenue IS NOT NULL
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,

    "sample_traffic_conversion_summary.csv": """
        SELECT
            COUNT(*) AS total_days,
            SUM(page_views)
                AS total_page_views,
            SUM(visitors)
                AS total_visitors,
            SUM(product_impressions)
                AS total_product_impressions,
            SUM(product_clicks)
                AS total_product_clicks,
            ROUND(
                AVG(conversion_rate),
                4
            ) AS average_conversion_rate,
            ROUND(
                AVG(aov),
                2
            ) AS average_order_value,
            ROUND(
                SUM(total_revenue),
                2
            ) AS total_revenue
        FROM shop_daily;
    """,

    "sample_channel_gmv_metrics.csv": """
        SELECT
            ROUND(
                SUM(
                    COALESCE(gmv, 0)
                ),
                2
            ) AS total_shop_gmv,

            ROUND(
                SUM(
                    COALESCE(
                        live_gmv_creator,
                        0
                    )
                ),
                2
            ) AS live_gmv_creator,

            ROUND(
                SUM(
                    COALESCE(
                        live_gmv_creator_direct,
                        0
                    )
                ),
                2
            ) AS live_gmv_creator_direct,

            ROUND(
                SUM(
                    COALESCE(
                        live_gmv_creator_indirect,
                        0
                    )
                ),
                2
            ) AS live_gmv_creator_indirect,

            ROUND(
                SUM(
                    COALESCE(
                        live_gmv_linked_account,
                        0
                    )
                ),
                2
            ) AS live_gmv_linked_account,

            ROUND(
                SUM(
                    COALESCE(
                        live_gmv_seller,
                        0
                    )
                ),
                2
            ) AS live_gmv_seller,

            ROUND(
                SUM(
                    COALESCE(
                        live_gmv_seller_indirect,
                        0
                    )
                ),
                2
            ) AS live_gmv_seller_indirect,

            ROUND(
                SUM(
                    COALESCE(
                        video_gmv_affiliate,
                        0
                    )
                ),
                2
            ) AS video_gmv_affiliate,

            ROUND(
                SUM(
                    COALESCE(
                        video_gmv_creator,
                        0
                    )
                ),
                2
            ) AS video_gmv_creator,

            ROUND(
                SUM(
                    COALESCE(
                        video_gmv_creator_indirect,
                        0
                    )
                ),
                2
            ) AS video_gmv_creator_indirect,

            ROUND(
                SUM(
                    COALESCE(
                        video_gmv_linked_account,
                        0
                    )
                ),
                2
            ) AS video_gmv_linked_account,

            ROUND(
                SUM(
                    COALESCE(
                        video_gmv_seller,
                        0
                    )
                ),
                2
            ) AS video_gmv_seller,

            ROUND(
                SUM(
                    COALESCE(
                        video_gmv_seller_indirect,
                        0
                    )
                ),
                2
            ) AS video_gmv_seller_indirect
        FROM shop_daily;
    """,

    "sample_data_quality_summary.csv": """
        SELECT
            COUNT(*) AS total_records,

            SUM(
                CASE
                    WHEN date IS NULL
                         OR TRIM(date) = ''
                    THEN 1
                    ELSE 0
                END
            ) AS missing_date_records,

            SUM(
                CASE
                    WHEN gmv IS NULL
                         OR gmv < 0
                    THEN 1
                    ELSE 0
                END
            ) AS invalid_gmv_records,

            SUM(
                CASE
                    WHEN orders IS NULL
                         OR orders < 0
                    THEN 1
                    ELSE 0
                END
            ) AS invalid_order_records,

            SUM(
                CASE
                    WHEN total_revenue IS NULL
                         OR total_revenue < 0
                    THEN 1
                    ELSE 0
                END
            ) AS invalid_revenue_records,

            SUM(
                CASE
                    WHEN conversion_rate IS NULL
                         OR conversion_rate < 0
                    THEN 1
                    ELSE 0
                END
            ) AS invalid_conversion_records,

            COUNT(*)
            - COUNT(DISTINCT date)
                AS duplicate_date_records
        FROM shop_daily;
    """
}


def remove_old_output_file() -> None:
    old_output_file = (
        OUTPUT_DIRECTORY
        / "sample_live_video_gmv_summary.csv"
    )

    if old_output_file.exists():
        old_output_file.unlink()

        print(
            "[INFO] ลบไฟล์เก่า: "
            "sample_live_video_gmv_summary.csv"
        )


def export_query_to_csv(
    connection: sqlite3.Connection,
    output_file: Path,
    query: str
) -> int:
    cursor = connection.execute(query)

    column_names = [
        description[0]
        for description in cursor.description
    ]

    rows = cursor.fetchall()

    with output_file.open(
        mode="w",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(column_names)

        writer.writerows(rows)

    return len(rows)


def main() -> None:
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"ไม่พบฐานข้อมูล: {DATABASE_PATH}"
        )

    OUTPUT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    remove_old_output_file()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        total_exported_rows = 0

        print(
            f"[INFO] Database: "
            f"{DATABASE_PATH}"
        )

        print(
            f"[INFO] Output directory: "
            f"{OUTPUT_DIRECTORY}"
        )

        print("-" * 70)

        for file_name, query in EXPORT_QUERIES.items():
            output_file = (
                OUTPUT_DIRECTORY
                / file_name
            )

            exported_rows = export_query_to_csv(
                connection=connection,
                output_file=output_file,
                query=query
            )

            total_exported_rows += exported_rows

            print(
                f"[SUCCESS] สร้าง "
                f"{file_name}: "
                f"{exported_rows} แถว"
            )

        print("-" * 70)

        print(
            "[SUCCESS] สร้าง Portfolio Outputs "
            "ครบทุกไฟล์แล้ว"
        )

        print(
            f"[INFO] จำนวนไฟล์: "
            f"{len(EXPORT_QUERIES)}"
        )

        print(
            f"[INFO] จำนวนแถวรวม: "
            f"{total_exported_rows}"
        )

    finally:
        connection.close()


if __name__ == "__main__":
    main()