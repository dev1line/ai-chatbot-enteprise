"""Shared pytest fixtures for RAG / chat integration tests."""
from __future__ import annotations

import pytest

from app.core.config import get_settings
from app.rag.vector_store import reset_vector_store

SECURITY_POLICY = b"""# Security Policy (Release v2.1)

## KMS Key Rotation
All encryption keys managed by KMS must be rotated periodically, once every 90 days.
The rotation process is automated via a pipeline and must be logged to the audit system.

## WAF Rules
The Web Application Firewall blocks common attack patterns: SQL injection, XSS, path traversal.
"""


@pytest.fixture
def rag_settings(monkeypatch):
    """Force in-memory providers so tests run without Azure or Qdrant."""
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("EMBEDDING_PROVIDER", "local")
    monkeypatch.setenv("VECTOR_DB_PROVIDER", "memory")
    get_settings.cache_clear()
    reset_vector_store()
    yield get_settings()
    reset_vector_store()
    get_settings.cache_clear()


@pytest.fixture
def security_policy_bytes() -> bytes:
    return SECURITY_POLICY
