from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_public_completion_without_login():
    response = client.post(
        "/api/public/chat/completions",
        json={"message": "Xin chao", "history": []},
    )

    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert "usage" in body
