"""Vector store abstraction (swappable via ENV `VECTOR_DB_PROVIDER`).

- `memory` : in-process, cosine — used for fast test/dev.
- `qdrant` : Qdrant container (already included in docker-compose).

Supports metadata filtering by `version` (immutable corpus).
"""
from __future__ import annotations

import math
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

COLLECTION = "documents"


@dataclass
class VectorRecord:
    id: str
    vector: list[float]
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class SearchHit:
    score: float
    payload: dict[str, Any]


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b, strict=False))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


class VectorStore(ABC):
    @abstractmethod
    async def ensure_collection(self, dim: int) -> None: ...

    @abstractmethod
    async def upsert(self, records: list[VectorRecord]) -> None: ...

    @abstractmethod
    async def search(
        self, vector: list[float], top_k: int, version: str | None = None
    ) -> list[SearchHit]: ...

    @abstractmethod
    async def delete_doc(self, doc_id: str, version: str) -> None: ...


class InMemoryVectorStore(VectorStore):
    def __init__(self) -> None:
        self._records: list[VectorRecord] = []

    async def ensure_collection(self, dim: int) -> None:
        return None

    async def upsert(self, records: list[VectorRecord]) -> None:
        self._records.extend(records)

    async def search(
        self, vector: list[float], top_k: int, version: str | None = None
    ) -> list[SearchHit]:
        hits = []
        for r in self._records:
            if version and r.payload.get("version") != version:
                continue
            hits.append(SearchHit(score=_cosine(vector, r.vector), payload=r.payload))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:top_k]

    async def delete_doc(self, doc_id: str, version: str) -> None:
        self._records = [
            r
            for r in self._records
            if not (r.payload.get("doc_id") == doc_id and r.payload.get("version") == version)
        ]


class QdrantVectorStore(VectorStore):
    def __init__(self) -> None:
        settings = get_settings()
        from qdrant_client import AsyncQdrantClient

        self._client = AsyncQdrantClient(url=settings.qdrant_url)
        self._dim: int | None = None

    async def ensure_collection(self, dim: int) -> None:
        from qdrant_client.models import Distance, VectorParams

        self._dim = dim
        existing = await self._client.get_collections()
        names = {c.name for c in existing.collections}
        if COLLECTION not in names:
            await self._client.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )
            logger.info("Created Qdrant collection '%s' (dim=%d)", COLLECTION, dim)

    async def upsert(self, records: list[VectorRecord]) -> None:
        from qdrant_client.models import PointStruct

        points = [
            PointStruct(id=str(uuid.uuid4()), vector=r.vector, payload=r.payload)
            for r in records
        ]
        await self._client.upsert(collection_name=COLLECTION, points=points)

    async def search(
        self, vector: list[float], top_k: int, version: str | None = None
    ) -> list[SearchHit]:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        flt = None
        if version:
            flt = Filter(
                must=[FieldCondition(key="version", match=MatchValue(value=version))]
            )
        results = await self._client.search(
            collection_name=COLLECTION,
            query_vector=vector,
            limit=top_k,
            query_filter=flt,
        )
        return [SearchHit(score=r.score, payload=r.payload or {}) for r in results]

    async def delete_doc(self, doc_id: str, version: str) -> None:
        from qdrant_client.models import (
            FieldCondition,
            Filter,
            FilterSelector,
            MatchValue,
        )

        try:
            await self._client.delete(
                collection_name=COLLECTION,
                points_selector=FilterSelector(
                    filter=Filter(
                        must=[
                            FieldCondition(key="doc_id", match=MatchValue(value=doc_id)),
                            FieldCondition(key="version", match=MatchValue(value=version)),
                        ]
                    )
                ),
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("delete_doc skipped: %s", exc)


_store: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _store
    if _store is not None:
        return _store
    settings = get_settings()
    if settings.vector_db_provider == "qdrant":
        _store = QdrantVectorStore()
    else:
        _store = InMemoryVectorStore()
    return _store
