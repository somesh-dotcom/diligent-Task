from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

SQL = """
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    o.order_id,
    o.order_date,
    p.product_name,
    oi.quantity,
    oi.unit_price AS price,
    pay.amount AS total_amount_paid
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
JOIN payments AS pay ON pay.order_id = o.order_id
ORDER BY o.order_date DESC, o.order_id DESC, oi.order_item_id ASC;
"""


def main(db_path: Path) -> None:
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(SQL, conn)
    print(df.head())
    print(f"{len(df)} rows returned.")


if __name__ == "__main__":
    main(Path("ecommerce.db"))

