import requests
from starlette.testclient import TestClient
from api.app import app

BASE_URL = "http://localhost:8000"
client = TestClient(app)

def test_health():
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200

def test_validate_password_weak():
    response = client.post("/validate-password", json={"password": "bla"})
    assert response.status_code == 200
    body = response.json()
    assert not body.get("valid")
    assert len(body.get("errors")) > 0


def test_validate_password_strong():
    response = client.post("/validate-password", json={"password": "GoodPassword123*"})
    assert response.status_code == 200
    body = response.json()
    assert body.get("valid")
    assert len(body.get("errors")) == 0