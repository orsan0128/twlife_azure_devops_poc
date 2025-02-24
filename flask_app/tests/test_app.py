import pytest
import sys
import os

# 確保 `flask_app` 目錄可以被找到
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from flask_app.app import app  # 確保這行可運行

@pytest.fixture
def client():
    """ 使用 Flask test_client 運行測試 """
    with app.test_client() as client:
        yield client

def test_home(client):
    """ 測試首頁是否回應 200 """
    response = client.get("/")
    assert response.status_code == 200
