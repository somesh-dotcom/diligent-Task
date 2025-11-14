from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


DB_PATH = Path("ecommerce.db")
CSV_FILES = {
    "customers": Path("customers.csv"),
    "products": Path("products.csv"),
    "orders": Path("orders.csv"),
    "order_items": Path("order_items.csv"),
    "payments": Path("payments.csv"),
}


CREATE_TABLE_STATEMENTS = {
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            country TEXT,
            signup_date DATE
        );
    """,
    "products": """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER NOT NULL,
            created_at DATE
        );
    """,
    "orders": """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            order_date DATE,
            shipping_address TEXT,
            status TEXT,
            total_amount REAL,
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        );
    """,
    "order_items": """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            line_total REAL NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
    """,
    "payments": """
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL,
            payment_date DATE,
            payment_method TEXT,
            amount REAL,
            currency TEXT,
            status TEXT,
            FOREIGN KEY(order_id) REFERENCES orders(order_id)
        );
    """,
}


def create_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    for table, ddl in CREATE_TABLE_STATEMENTS.items():
        cursor.executescript(ddl)
    conn.commit()


def load_csv_to_table(conn: sqlite3.Connection, table_name: str, csv_path: Path) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Inserted {len(df)} rows into {table_name}.")


def main(base_dir: Path) -> None:
    resolved_paths = {name: (base_dir / path) for name, path in CSV_FILES.items()}
    with sqlite3.connect(base_dir / DB_PATH) as conn:
        create_tables(conn)
        for table_name, csv_path in resolved_paths.items():
            load_csv_to_table(conn, table_name, csv_path)
        print(f"SQLite database ready at {(base_dir / DB_PATH).resolve()}")


if __name__ == "__main__":
    main(Path("."))

