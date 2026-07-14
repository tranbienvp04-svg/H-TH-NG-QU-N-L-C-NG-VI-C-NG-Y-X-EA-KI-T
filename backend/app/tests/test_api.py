from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_endpoint():
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "123456"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"] == "demo-token"


def test_tasks_endpoint():
    response = client.get("/api/v1/tasks")
    assert response.status_code == 200
