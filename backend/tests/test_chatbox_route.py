from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chatbox_route_ok():
    response = client.get("/chatbox")
    assert response.status_code == 200
    assert "Backend Chatbox Test" in response.text
