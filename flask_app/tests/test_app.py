import pytest
import requests
from flask_app.app import app

BASE_URL = "http://127.0.0.1:5000"  # 確保 Flask 運行的 URL 正確

@pytest.fixture
def client():
    """ 使用 Flask test_client 運行測試，避免實際發送 HTTP 請求 """
    with app.test_client() as client:
        yield client

def test_home(client):
    """ 使用 test_client 直接測試 Flask API，而不是發送外部請求 """
    response = client.get("/")
    assert response.status_code == 200