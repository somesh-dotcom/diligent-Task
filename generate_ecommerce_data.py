from __future__ import annotations

import random
from datetime import date
from pathlib import Path
from typing import Dict, List

import pandas as pd
from faker import Faker


def generate_customers(fake: Faker, count: int) -> List[Dict]:
    customers = []
    for customer_id in range(1, count + 1):
        customers.append(
            {
                "customer_id": customer_id,
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.unique.email(),
                "phone": fake.phone_number(),
                "country": fake.country(),
                "signup_date": fake.date_between(start_date="-2y", end_date="today").isoformat(),
            }
        )
    return customers


def generate_products(fake: Faker, count: int) -> List[Dict]:
    categories = [
        "Electronics",
        "Home & Kitchen",
        "Apparel",
        "Beauty",
        "Sports",
        "Books",
        "Toys",
        "Grocery",
    ]
    products = []
    for product_id in range(1, count + 1):
        base_price = round(random.uniform(5.0, 500.0), 2)
        products.append(
            {
                "product_id": product_id,
                "product_name": fake.catch_phrase(),
                "category": random.choice(categories),
                "price": base_price,
                "stock_quantity": random.randint(10, 500),
                "created_at": fake.date_between(start_date="-3y", end_date="today").isoformat(),
            }
        )
    return products


def generate_orders(fake: Faker, count: int, customer_ids: List[int]) -> List[Dict]:
    statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
    orders = []
    for order_id in range(1, count + 1):
        order_date = fake.date_between(start_date="-18m", end_date="today")
        shipping_address = fake.address().replace("\n", ", ")
        orders.append(
            {
                "order_id": order_id,
                "customer_id": random.choice(customer_ids),
                "order_date": order_date.isoformat(),
                "shipping_address": shipping_address,
                "status": random.choices(statuses, weights=[10, 20, 30, 35, 5])[0],
                "total_amount": 0.0,  # placeholder set later
            }
        )
    return orders


def generate_order_items(orders: List[Dict], product_lookup: Dict[int, Dict]) -> List[Dict]:
    order_totals = {order["order_id"]: 0.0 for order in orders}
    order_items = []
    for order in orders:
        num_items = random.randint(1, 5)
        chosen_products = random.sample(list(product_lookup.keys()), k=num_items)
        for product_id in chosen_products:
            product = product_lookup[product_id]
            unit_price = round(product["price"] * random.uniform(0.9, 1.1), 2)
            quantity = random.randint(1, 4)
            line_total = round(unit_price * quantity, 2)
            order_totals[order["order_id"]] += line_total
            order_items.append(
                {
                    "order_item_id": len(order_items) + 1,
                    "order_id": order["order_id"],
                    "product_id": product_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_total": line_total,
                }
            )
    for order in orders:
        order["total_amount"] = round(order_totals[order["order_id"]], 2)
    return order_items


def generate_payments(fake: Faker, orders: List[Dict]) -> List[Dict]:
    methods = ["credit_card", "paypal", "bank_transfer", "gift_card"]
    statuses = ["completed", "pending", "failed", "refunded"]
    payments = []
    for order in orders:
        order_date = date.fromisoformat(order["order_date"])
        payments.append(
            {
                "payment_id": len(payments) + 1,
                "order_id": order["order_id"],
                "payment_date": fake.date_between(
                    start_date=order_date, end_date="today"
                ).isoformat(),
                "payment_method": random.choices(methods, weights=[50, 25, 15, 10])[0],
                "amount": order["total_amount"],
                "currency": "USD",
                "status": random.choices(statuses, weights=[70, 15, 10, 5])[0],
            }
        )
    return payments


def save_to_csv(rows: List[Dict], destination: Path) -> None:
    pd.DataFrame(rows).to_csv(destination, index=False)


def main(output_dir: Path) -> None:
    fake = Faker()
    Faker.seed(42)
    random.seed(42)

    counts = {
        "customers": 120,
        "products": 80,
        "orders": 160,
    }

    customers = generate_customers(fake, counts["customers"])
    products = generate_products(fake, counts["products"])
    product_lookup = {product["product_id"]: product for product in products}
    orders = generate_orders(fake, counts["orders"], [c["customer_id"] for c in customers])
    order_items = generate_order_items(orders, product_lookup)
    payments = generate_payments(fake, orders)

    output_dir.mkdir(parents=True, exist_ok=True)
    save_to_csv(customers, output_dir / "customers.csv")
    save_to_csv(products, output_dir / "products.csv")
    save_to_csv(orders, output_dir / "orders.csv")
    save_to_csv(order_items, output_dir / "order_items.csv")
    save_to_csv(payments, output_dir / "payments.csv")

    print(f"Synthetic datasets saved to {output_dir.resolve()}")


if __name__ == "__main__":
    main(Path("."))

