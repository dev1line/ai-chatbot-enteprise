from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import health


def _app() -> FastAPI:
    app = FastAPI()
    app.include_router(health.router)
    return app


def test_health_ok():
    client = TestClient(_app())
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "app_env" in body
