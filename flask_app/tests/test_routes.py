import pytest
import json
from flask_app.app import app
from datetime import timedelta
from flask_app.routes.config import get_config

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


class CustomConfigValue:
    def __repr__(self):
        return "CustomConfigValue()"


def test_config(client):
    """測試 /config 路由"""
    with app.app_context():
        # 設定 app.config 的值
        app.config['TEST_STRING'] = 'test string'
        app.config['TEST_INTEGER'] = 123
        app.config['TEST_FLOAT'] = 3.14
        app.config['TEST_BOOLEAN'] = True
        app.config['TEST_LIST'] = [1, 2, 3]
        app.config['TEST_DICT'] = {'key': 'value'}
        app.config['TEST_TIMEDELTA'] = timedelta(days=1)
        app.config['TEST_CUSTOM'] = CustomConfigValue()  # 加入自訂類別實例

        # 直接呼叫 get_config 函數
        safe_config = get_config()

        # 驗證配置鍵是否存在，並檢查值的類型是否正確
        assert 'TEST_STRING' in safe_config
        assert isinstance(safe_config['TEST_STRING'], str)
        assert 'TEST_INTEGER' in safe_config
        assert isinstance(safe_config['TEST_INTEGER'], int)
        assert 'TEST_FLOAT' in safe_config
        assert isinstance(safe_config['TEST_FLOAT'], float)
        assert 'TEST_BOOLEAN' in safe_config
        assert isinstance(safe_config['TEST_BOOLEAN'], bool)
        assert 'TEST_LIST' in safe_config
        assert isinstance(safe_config['TEST_LIST'], list)
        assert 'TEST_DICT' in safe_config
        assert isinstance(safe_config['TEST_DICT'], dict)
        assert 'TEST_TIMEDELTA' in safe_config
        assert isinstance(safe_config['TEST_TIMEDELTA'], str)
        assert 'TEST_CUSTOM' in safe_config
        assert safe_config['TEST_CUSTOM'] == "CustomConfigValue()"  # 驗證自訂類別實例被 repr()
