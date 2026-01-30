import pandas as pd
from db.db_config import get_connection

EXPORT_PATH = "exports/tableau_data/"

def export_table(table_name):
    conn = get_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    df.to_csv(f"{EXPORT_PATH}{table_name}.csv", index=False)
    conn.close()
    print(f"{table_name} exported")

def main():
    tables = [
        "customers",
        "products",
        "orders",
        "services",
        "billing",
        "usage_records",
        "provisioning_logs"
    ]

    for table in tables:
        export_table(table)

if __name__ == "__main__":
    main()
