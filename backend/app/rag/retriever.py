from __future__ import annotations

from app.core.config import get_settings
from app.rag.embeddings import get_embedding_provider
from app.rag.ingestion import Chunk
from app.rag.vector_store import SearchHit, VectorRecord, get_vector_store


async def index_chunks(chunks: list[Chunk]) -> int:
    """Embed + upsert chunks into the vector store. Returns the number of indexed chunks.

    Immutable corpus: delete the old version of the same doc before re-indexing (idempotent).
    """
    if not chunks:
        return 0
    embedder = get_embedding_provider()
    store = get_vector_store()
    await store.ensure_collection(embedder.dim)

    meta0 = chunks[0].metadata
    doc_id, version = meta0.get("doc_id"), meta0.get("version")
    if doc_id and version:
        await store.delete_doc(doc_id, version)

    vectors = await embedder.embed_many([c.text for c in chunks])
    records = [
        VectorRecord(id="", vector=v, payload={**c.metadata, "text": c.text})
        for c, v in zip(chunks, vectors, strict=False)
    ]
    await store.upsert(records)
    return len(records)


async def retrieve(query: str, version: str | None = None) -> list[SearchHit]:
    settings = get_settings()
    embedder = get_embedding_provider()
    store = get_vector_store()
    qv = await embedder.embed(query)
    hits = await store.search(qv, top_k=settings.rag_top_k, version=version)
    return [h for h in hits if h.score >= settings.rag_score_threshold]
