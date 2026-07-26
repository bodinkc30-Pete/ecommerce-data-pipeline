from pathlib import Path
import sqlite3


DATABASE_FILE = Path("data/processed/ecommerce.db")
TABLE_NAME = "shop_daily"


connection = sqlite3.connect(DATABASE_FILE)

row_count = connection.execute(
    f"SELECT COUNT(*) FROM {TABLE_NAME}"
).fetchone()[0]

summary = connection.execute(
    f"""
    SELECT
        SUM(gmv),
        SUM(orders),
        AVG(gmv)
    FROM {TABLE_NAME}
    """
).fetchone()

highest_gmv_day = connection.execute(
    f"""
    SELECT
        date,
        gmv
    FROM {TABLE_NAME}
    ORDER BY gmv DESC
    LIMIT 1
    """
).fetchone()

highest_orders_day = connection.execute(
    f"""
    SELECT
        date,
        orders
    FROM {TABLE_NAME}
    ORDER BY orders DESC
    LIMIT 1
    """
).fetchone()

top_gmv_days = connection.execute(
    f"""
    SELECT
        date,
        gmv
    FROM {TABLE_NAME}
    ORDER BY gmv DESC
    LIMIT 5
    """
).fetchall()

top_order_days = connection.execute(
    f"""
    SELECT
        date,
        orders
    FROM {TABLE_NAME}
    ORDER BY orders DESC
    LIMIT 5
    """
).fetchall()

monthly_summary = connection.execute(
    f"""
    SELECT
        substr(date, 1, 7) AS month,
        SUM(gmv) AS total_gmv,
        SUM(orders) AS total_orders
    FROM {TABLE_NAME}
    GROUP BY substr(date, 1, 7)
    ORDER BY month
    """
).fetchall()

average_gmv_per_order = summary[0] / summary[1]

connection.close()


print(f"Database rows: {row_count}")
print(f"Total GMV: {summary[0]:.2f}")
print(f"Total orders: {summary[1]}")
print(f"Average daily GMV: {summary[2]:.2f}")
print(f"Average GMV per order: {average_gmv_per_order:.2f}")

print(f"Highest GMV date: {highest_gmv_day[0]}")
print(f"Highest GMV: {highest_gmv_day[1]:.2f}")

print(f"Highest orders date: {highest_orders_day[0]}")
print(f"Highest orders: {highest_orders_day[1]}")

print("\nTop 5 GMV days")
for date, gmv in top_gmv_days:
    print(f"{date} | {gmv:.2f}")

print("\nTop 5 order days")
for date, orders in top_order_days:
    print(f"{date} | {orders}")

print("\nMonthly summary")
print("month | total_gmv | total_orders")

for month, total_gmv, total_orders in monthly_summary:
    print(f"{month} | {total_gmv:.2f} | {total_orders}")