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