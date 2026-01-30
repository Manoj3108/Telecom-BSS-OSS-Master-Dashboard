import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="telecom_bss_oss",
        user="postgres",
        password="admin"  # Replace with your actual password
    )
