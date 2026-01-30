import random
from datetime import timedelta
from faker import Faker
from db.db_config import get_connection

fake = Faker()

def generate_usage(records_per_service=25):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT service_id, activation_date
        FROM services
        WHERE service_status = 'ACTIVE'
    """)
    services = cursor.fetchall()

    total_records = 0

    for service_id, activation_date in services:
        for _ in range(records_per_service):
            usage_date = fake.date_between(
                start_date=activation_date.date(),
                end_date="today"
            )
            data_used = round(random.uniform(10, 500), 2)  # MB

            cursor.execute("""
                INSERT INTO usage_records (service_id, usage_date, data_used_mb)
                VALUES (%s, %s, %s)
            """, (service_id, usage_date, data_used))

            total_records += 1

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{total_records} usage records generated successfully.")

if __name__ == "__main__":
    generate_usage(records_per_service=30)
