import random
from faker import Faker
from db.db_config import get_connection

fake = Faker()

def run_provisioning():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch ACTIVE orders not yet provisioned
    cursor.execute("""
        SELECT o.order_id, o.customer_id, o.product_id
        FROM orders o
        LEFT JOIN services s ON o.order_id = s.order_id
        WHERE o.order_status = 'ACTIVE'
          AND s.order_id IS NULL
    """)
    orders = cursor.fetchall()

    success_count = 0
    failure_count = 0

    for order_id, customer_id, product_id in orders:
        provision_status = random.choices(
            ["SUCCESS", "FAILED"],
            weights=[95, 5]
        )[0]

        response_time = random.randint(200, 3000)

        if provision_status == "SUCCESS":
            activation_date = fake.date_time_between(start_date="-30d", end_date="now")

            # Create service
            cursor.execute("""
                INSERT INTO services (order_id, customer_id, product_id, activation_date, service_status)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, customer_id, product_id, activation_date, "ACTIVE"))

            error_message = None
            success_count += 1
        else:
            error_message = "Network provisioning failure"
            failure_count += 1

        # Insert provisioning log
        cursor.execute("""
            INSERT INTO provisioning_logs (order_id, provision_status, response_time_ms, error_message)
            VALUES (%s, %s, %s, %s)
        """, (order_id, provision_status, response_time, error_message))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Provisioning completed: {success_count} success, {failure_count} failed.")

if __name__ == "__main__":
    run_provisioning()
