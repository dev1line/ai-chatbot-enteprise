"""RAG orchestrator happy-path and edge-case tests."""
from __future__ import annotations

import pytest

from app.orchestration.orchestrator import answer_query
from app.rag.ingestion import load_text
from app.rag.retriever import index_chunks, retrieve


@pytest.mark.asyncio
async def test_index_and_retrieve_security_policy(rag_settings, security_policy_bytes):
    chunks = load_text(
        security_policy_bytes,
        doc_id="SEC-1",
        version="v2.1",
        source="security-policy.md",
    )
    indexed = await index_chunks(chunks)
    assert indexed == len(chunks)

    hits = await retrieve("How often does KMS key rotation happen?", version="v2.1")
    assert hits
    assert hits[0].payload["doc_id"] == "SEC-1"
    assert "90 days" in hits[0].payload.get("text", "")


@pytest.mark.asyncio
async def test_answer_query_happy_path(rag_settings, security_policy_bytes):
    chunks = load_text(
        security_policy_bytes,
        doc_id="SEC-1",
        version="v2.1",
        source="security-policy.md",
    )
    await index_chunks(chunks)

    answer, citations = await answer_query(
        "How often are KMS keys rotated?",
        version="v2.1",
    )

    assert citations
    assert citations[0].doc_id == "SEC-1"
    assert citations[0].version == "v2.1"
    assert "90 days" in answer.lower() or "90 days" in citations[0].snippet.lower()
    assert "[1]" in answer or "retrieved documents" in answer.lower()


@pytest.mark.asyncio
async def test_answer_query_no_hits_returns_safe_message(rag_settings):
    answer, citations = await answer_query("What is the meaning of life?")
    assert citations == []
    assert "no relevant information" in answer.lower()


@pytest.mark.asyncio
async def test_answer_query_version_filter_excludes_other_versions(
    rag_settings, security_policy_bytes
):
    v21 = load_text(security_policy_bytes, "SEC-1", "v2.1", "sec.md")
    v10 = load_text(b"Old policy: KMS rotation every 365 days.", "SEC-1", "v1.0", "old.md")
    await index_chunks(v21)
    await index_chunks(v10)

    answer, citations = await answer_query("KMS key rotation frequency", version="v2.1")
    assert citations
    assert all(c.version == "v2.1" for c in citations)
    assert "365" not in answer
