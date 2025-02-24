import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_home():
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Azure DevOps & Flask!"}