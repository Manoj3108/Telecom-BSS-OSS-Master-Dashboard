import random
from datetime import date
from db.db_config import get_connection

def generate_billing():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.service_id, s.customer_id, s.order_id, p.price
        FROM services s
        JOIN products p ON s.product_id = p.product_id
    """)
    services = cursor.fetchall()

    for service_id, customer_id, order_id, price in services:
        payment_status = random.choices(
            ["PAID", "UNPAID"],
            weights=[80, 20]
        )[0]

        cursor.execute("""
            INSERT INTO billing (customer_id, order_id, bill_amount, bill_date, payment_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, order_id, price, date.today(), payment_status))

    conn.commit()
    cursor.close()
    conn.close()

    print("Billing records generated successfully.")

if __name__ == "__main__":
    generate_billing()
