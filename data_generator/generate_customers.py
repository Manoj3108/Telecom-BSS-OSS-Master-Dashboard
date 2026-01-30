from faker import Faker
import random
from db.db_config import get_connection

fake = Faker()

def generate_customers(n=200):
    conn = get_connection()
    cursor = conn.cursor()

    for _ in range(n):
        name = fake.name()
        customer_type = random.choice(["PREPAID", "POSTPAID"])
        status = random.choices(
            ["ACTIVE", "SUSPENDED"],
            weights=[85, 15]
        )[0]
        created_date = fake.date_between(start_date="-60d", end_date="today")

        cursor.execute(
            """
            INSERT INTO customers (customer_name, customer_type, status, created_date)
            VALUES (%s, %s, %s, %s)
            """,
            (name, customer_type, status, created_date)
        )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{n} customers inserted successfully.")

if __name__ == "__main__":
    generate_customers(300)
