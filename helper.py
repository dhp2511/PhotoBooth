import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("db.sqlite3")

# Get table names
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Export each table to CSV
for table in tables:
    table_name = table[0]
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    df.to_csv(f"{table_name}.csv", index=False)
    print(f"Exported {table_name} to {table_name}.csv")

# Close connection
conn.close()
