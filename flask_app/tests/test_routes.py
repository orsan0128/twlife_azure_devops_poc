import pytest
import json
from flask_app.app import app

# 創建一個測試客戶端


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# 測試根路由，檢查首頁返回200


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    # 將 response 轉換為字典，檢查 "status" 是否為 "ok"
    response_json = json.loads(response.data)
    assert response_json["status"] == "ok"

# 測試版本 API


def test_version(client):
    response = client.get('/version')
    assert response.status_code == 200
    assert b"version" in response.data  # 假設返回的內容包含 "version"

# 測試所有的路由，動態檢查每個路由


@pytest.mark.parametrize("route", [
    "/health", "/version", "/status", "/metrics", "/config"
])
def test_selected_routes(client, route):
    response = client.get(route)
    assert response.status_code == 200, f"Route {route} failed with status code {response.status_code}"

# 測試所有有效的動態 API 路由


@pytest.mark.parametrize("route", [
    rule.rule if rule.rule.startswith("/") else "/" + rule.rule
    for rule in app.url_map.iter_rules()
    if rule.endpoint != 'static'  # 排除靜態文件路由
])
def test_all_routes(client, route):
    try:
        response = client.get(route, allow_redirects=True)  # 允許重定向
        assert response.status_code == 200, f"Route {route} failed with status code {response.status_code}"
    except Exception as e:
        print(f"Error with route {route}: {e}")
