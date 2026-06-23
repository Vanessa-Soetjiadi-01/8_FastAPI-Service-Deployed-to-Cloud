import os
from dotenv import load_dotenv
import psycopg
from fastapi import FastAPI, HTTPException

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

app = FastAPI()

def get_connection():
    return psycopg.connect(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "hello"}

@app.get("/stocks")
def list_stocks():
    with get_connection() as conn:
        with conn.cursor() as cur:
            tickers = [row[0] for row in cur.execute("SELECT DISTINCT ticker FROM stocks").fetchall()]
    return {"tickers": tickers}

@app.get("/stocks/compare")
def compare_stocks(tickers: str, days: int = 30):
    with get_connection() as conn:
        with conn.cursor() as cur:
            ticker_list = tickers.split(',')
            result = {}
            for ticker in ticker_list:
                rows = cur.execute("SELECT ticker, date, open, high, low, close, volume, ma_7, ma_30, daily_change FROM stocks WHERE ticker=%s ORDER BY date DESC LIMIT %s", (ticker, days)).fetchall()
                column_names = [d.name for d in cur.description]
                result[ticker] = [dict(zip(column_names, row)) for row in rows]
    return result

@app.get("/stocks/top-movers")
def top_movers():
    with get_connection() as conn:
        with conn.cursor() as cur:
            tickers = [row[0] for row in cur.execute("SELECT DISTINCT ticker FROM stocks").fetchall()]

            result = [cur.execute("SELECT ticker, date, open, high, low, close, volume, ma_7, ma_30, daily_change FROM stocks WHERE ticker=%s ORDER BY date DESC LIMIT 1", (ticker,)).fetchone() for ticker in tickers]
            column_names = [d.name for d in cur.description]
            result = [dict(zip(column_names, row)) for row in result]
    return sorted(result, key=lambda r: r["daily_change"], reverse=True)

@app.get("/stocks/{ticker}")
def get_stock(ticker: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
                row = cur.execute("SELECT ticker, date, open, high, low, close, volume, ma_7, ma_30, daily_change FROM stocks WHERE ticker = %s ORDER BY date DESC LIMIT 1", (ticker,)).fetchone()
                if row is None:
                    raise HTTPException(status_code=404, detail=f"Ticker '{ticker}' not found")
                column_names = [d.name for d in cur.description]
    return dict(zip(column_names, row))

@app.get("/stocks/{ticker}/history")
def get_history(ticker: str, days: int = 30):
    with get_connection() as conn:
        with conn.cursor() as cur:
            rows = cur.execute("SELECT ticker, date, open, high, low, close, volume, ma_7, ma_30, daily_change FROM stocks WHERE ticker=%s ORDER BY date DESC LIMIT %s", (ticker, days)).fetchall()
            column_names = [d.name for d in cur.description]
    return [dict(zip(column_names, row)) for row in rows]