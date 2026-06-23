import os
import sqlite3
from dotenv import load_dotenv
import psycopg

# db url from .env
load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

SQLITE_PATH = "../7_python_etl_data_pipeline/stock.db"
sqlite_conn = sqlite3.connect(SQLITE_PATH)

# fetched the local data from my other project
rows = sqlite_conn.execute(
    "SELECT ticker, date, open, high, low, close, volume, ma_7, ma_30, daily_change "
    "FROM stocks GROUP BY ticker, date"
).fetchall()
print(f"Read {len(rows)} rows from stock.db")

# cleaned the data
cleaned = [
  (t, d, o, h, l, c, int(v), m7, m30, dc)
  for (t, d, o, h, l, c, v, m7, m30, dc) in rows
]

# connect to db and created the db
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
