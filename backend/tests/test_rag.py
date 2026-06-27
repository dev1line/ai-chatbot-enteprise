import pytest

from app.rag.embeddings import LocalHashingEmbedding
from app.rag.ingestion import chunk_text, load_text
from app.rag.retriever import index_chunks, retrieve
from app.rag.vector_store import InMemoryVectorStore, VectorRecord


def test_chunk_text_overlap():
    text = "a" * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=120)
    assert len(chunks) >= 2
    assert all(len(c) <= 800 for c in chunks)


def test_load_text_metadata():
    data = b"KMS key rotation 90 days policy"
    chunks = load_text(data, doc_id="SEC-1", version="v2.1", source="sec.md")
    assert chunks
    assert chunks[0].metadata["doc_id"] == "SEC-1"
    assert chunks[0].metadata["version"] == "v2.1"
    assert chunks[0].metadata["type"] == "text"


@pytest.mark.asyncio
async def test_index_chunks_idempotent_reindex(rag_settings):
    chunks = load_text(b"KMS rotation 90 days", "SEC-1", "v2.1", "sec.md")
    first = await index_chunks(chunks)
    second = await index_chunks(chunks)
    assert first == second == len(chunks)
    hits = await retrieve("KMS rotation", version="v2.1")
    assert hits
    assert hits[0].payload["doc_id"] == "SEC-1"


@pytest.mark.asyncio
async def test_memory_vector_store_search_and_version_filter():
    emb = LocalHashingEmbedding(dim=128)
    store = InMemoryVectorStore()

    docs = [
        ("KMS key rotation occurs every 90 days", {"version": "v2.1", "doc_id": "SEC"}),
        ("Restart payment-service using rollout", {"version": "v2.1", "doc_id": "OPS"}),
        ("Old unrelated document", {"version": "v1.0", "doc_id": "OLD"}),
    ]
    records = []
    for text, meta in docs:
        vec = await emb.embed(text)
        records.append(VectorRecord(id="", vector=vec, payload={**meta, "text": text}))
    await store.upsert(records)

    qv = await emb.embed("How often does KMS key rotation happen?")
    hits = await store.search(qv, top_k=2)
    assert hits
    assert hits[0].payload["doc_id"] == "SEC"

    hits_v1 = await store.search(qv, top_k=5, version="v1.0")
    assert all(h.payload["version"] == "v1.0" for h in hits_v1)
