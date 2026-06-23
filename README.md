# 8_FastAPI-Service-Deployed-to-Cloud

![CI](https://github.com/Vanessa-Soetjiadi-01/8_FastAPI-Service-Deployed-to-Cloud/actions/workflows/ci.yml/badge.svg)

A FastAPI REST API serving ASX stock data (OHLCV, moving averages, daily change)
from a Postgres database, deployed live on Render with automated tests in CI.

**Live API:** https://asx-stock-api.onrender.com/docs

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/stocks` | List all available tickers |
| GET | `/stocks/{ticker}` | Latest OHLCV + moving averages for one ticker |
| GET | `/stocks/{ticker}/history?days=30` | Recent history for one ticker (default 30 days) |
