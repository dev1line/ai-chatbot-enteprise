"""Chat API integration tests (repos mocked, RAG pipeline real)."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.chat import router as chat_router
from app.core.deps import get_current_user
from app.rag.ingestion import load_text
from app.rag.retriever import index_chunks
from app.schemas.auth import CurrentUser


def _build_chat_app() -> FastAPI:
    app = FastAPI()

    async def fake_user() -> CurrentUser:
        return CurrentUser(id="user-1", role="ENGINEER")

    app.dependency_overrides[get_current_user] = fake_user
    app.include_router(chat_router)
    return app


@pytest.fixture
def chat_client(rag_settings, security_policy_bytes, monkeypatch):
    mock_conv = MagicMock()
    mock_conv.id = "conv-test-1"
    mock_conv.userId = "user-1"

    mock_conv_repo = AsyncMock()
    mock_conv_repo.create = AsyncMock(return_value=mock_conv)
    mock_conv_repo.get = AsyncMock(return_value=mock_conv)

    mock_msg_repo = AsyncMock()
    mock_msg_repo.add = AsyncMock()

    import app.api.chat as chat_module

    monkeypatch.setattr(chat_module, "ConversationRepository", lambda: mock_conv_repo)
    monkeypatch.setattr(chat_module, "MessageRepository", lambda: mock_msg_repo)

    async def _seed():
        chunks = load_text(
            security_policy_bytes,
            doc_id="SEC-1",
            version="v2.1",
            source="security-policy.md",
        )
        await index_chunks(chunks)

    import asyncio

    asyncio.run(_seed())

    yield TestClient(_build_chat_app()), mock_conv_repo, mock_msg_repo


def test_chat_happy_path_returns_answer_and_citations(chat_client):
    client, conv_repo, msg_repo = chat_client
    resp = client.post(
        "/api/chat",
        json={"message": "How often are KMS keys rotated?", "version": "v2.1"},
        headers={"Authorization": "Bearer fake-token"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["conversation_id"] == "conv-test-1"
    assert body["answer"]
    assert len(body["citations"]) >= 1
    assert body["citations"][0]["doc_id"] == "SEC-1"
    assert "90 days" in body["answer"].lower() or any(
        "90" in (c.get("snippet") or "") for c in body["citations"]
    )
    conv_repo.create.assert_awaited_once()
    assert msg_repo.add.await_count == 2


def test_chat_reuses_existing_conversation(chat_client):
    client, conv_repo, _msg_repo = chat_client
    resp = client.post(
        "/api/chat",
        json={
            "message": "What does WAF block?",
            "conversation_id": "conv-test-1",
            "version": "v2.1",
        },
        headers={"Authorization": "Bearer fake-token"},
    )
    assert resp.status_code == 200
    conv_repo.get.assert_awaited()
    conv_repo.create.assert_not_awaited()


def test_chat_conversation_not_found(chat_client):
    client, conv_repo, _msg_repo = chat_client
    conv_repo.get = AsyncMock(return_value=None)
    resp = client.post(
        "/api/chat",
        json={"message": "hello", "conversation_id": "missing-id"},
        headers={"Authorization": "Bearer fake-token"},
    )
    assert resp.status_code == 404
