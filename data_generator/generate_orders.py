import random
from faker import Faker
from db.db_config import get_connection

fake = Faker()

ORDER_STATUSES = [
    "CREATED",
    "VALIDATED",
    "BILLED",
    "PROVISIONING",
    "ACTIVE",
    "FAILED"
]

def generate_orders(min_orders=500, max_orders=2000):
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch customers
    cursor.execute("SELECT customer_id FROM customers")
    customers = cursor.fetchall()

    # Fetch products
    cursor.execute("SELECT product_id FROM products")
    products = cursor.fetchall()

    total_orders = random.randint(min_orders, max_orders)

    for _ in range(total_orders):
        customer_id = random.choice(customers)[0]
        product_id = random.choice(products)[0]

        final_status = random.choices(
            ["ACTIVE", "FAILED"],
            weights=[90, 10]
        )[0]

        order_status = final_status
        order_date = fake.date_time_between(start_date="-45d", end_date="now")

        cursor.execute(
            """
            INSERT INTO orders (customer_id, product_id, order_status, order_date)
            VALUES (%s, %s, %s, %s)
            """,
            (customer_id, product_id, order_status, order_date)
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{total_orders} orders generated successfully.")

if __name__ == "__main__":
    generate_orders()
