from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_list_stocks():
  response = client.get("/stocks")
  assert response.status_code == 200

  tickers = response.json()["tickers"]
  assert "CBA.AX" in tickers
  assert "WOW.AX" in tickers

def test_get_stock():
  response = client.get("/stocks/CBA.AX")
  assert response.status_code == 200 
  assert response.json()["ticker"] == "CBA.AX"

def test_get_stock_not_found():
  response = client.get("/stocks/FAKE")
  assert response.status_code == 404

def test_history():
  response = client.get("/stocks/CBA.AX/history?days=7")
  assert response.status_code == 200
  assert len(response.json()) == 7

def test_compare():
  response = client.get("/stocks/compare?tickers=CBA.AX,BHP.AX&days=5")
  assert response.status_code == 200

  data = response.json()
  assert "CBA.AX" in data
  assert "BHP.AX" in data
  assert len(data["CBA.AX"]) == 5

def test_top_movers():
  response = client.get("/stocks/top-movers")
  assert response.status_code == 200

  data = response.json()
  assert len(data) == 6
  changes = [row["daily_change"] for row in data]
  assert changes == sorted(changes, reverse=True)