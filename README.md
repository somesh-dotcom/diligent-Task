Synthetic e-commerce dataset generator and SQLite loader.

## Contents
- `generate_ecommerce_data.py` – builds realistic customers, products, orders, order items, and payments CSVs using Faker.
- `load_to_sqlite.py` – creates `ecommerce.db`, defines tables with FK constraints, and loads the CSVs via pandas.
- `query.sql` – sample analytics join across all tables.
- `run_query.py` – executes `query.sql` through sqlite3/pandas and prints the resulting DataFrame.

## Quick Start
1. Install deps: `pip3 install pandas faker`.
2. Generate CSVs: `python3 generate_ecommerce_data.py`.
3. Load into SQLite: `python3 load_to_sqlite.py`.
4. Run the report: `python3 run_query.py` (ensures `ecommerce.db` exists from step 3).

All outputs land in the repository root (`*.csv` and `ecommerce.db`). Customize row counts or table schemas directly inside the scripts as needed.

