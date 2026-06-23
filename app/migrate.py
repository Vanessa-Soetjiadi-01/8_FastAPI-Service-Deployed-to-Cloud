import os
import sqlite3
from dotenv import load_dotenv
import psycopg

# fetched the URL from .env
load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

SQLITE_PATH = "../7_python_etl_data_pipeline/stock.db"
sqlite_conn = sqlite3.connect(SQLITE_PATH)
rows = sqlite_conn.execute(
    "SELECT ticker, date, open, high, low, close, volume, ma_7, ma_30, daily_change FROM stocks"
).fetchall()
print(f"Read {len(rows)} rows from stock.db")

# cleaned the data and modified the data type for volume
cleaned = [
  (t, d, o, h, l, c, int(v), m7, m30, dc)
  for (t, d, o, h, l, c, v, m7, m30, dc) in rows
]

with psycopg.connect(DATABASE_URL) as conn:
    print("Connected to Neon!")
    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS stocks")
        cur.execute("""
            CREATE TABLE stocks (
                ticker        TEXT,
                date          TIMESTAMP,
                open          DOUBLE PRECISION,
                high          DOUBLE PRECISION,
                low           DOUBLE PRECISION,
                close         DOUBLE PRECISION,
                volume        BIGINT,
                ma_7          DOUBLE PRECISION,
                ma_30         DOUBLE PRECISION,
                daily_change  DOUBLE PRECISION
            )
        """)

        insert_sql = "INSERT INTO stocks VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.executemany(insert_sql, cleaned)
        print(f"Inserted {len(cleaned)} rows into Neon")
