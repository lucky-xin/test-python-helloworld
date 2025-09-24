from fastapi.testclient import TestClient

import server


def _client() -> TestClient:
    return TestClient(server.app)


def test_root():
    c = _client()
    r = c.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["message"].startswith("Hello")
    assert data["service"] == "test-python-helloworld"


def test_health():
    c = _client()
    r = c.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"


def test_info_and_hello():
    c = _client()
    r = c.get("/info")
    assert r.status_code == 200
    data = r.json()
    assert "app_name" in data
    assert "environment" in data

    r2 = c.get("/hello/world")
    assert r2.status_code == 200
    assert r2.json()["message"] == "Hello, world!"

