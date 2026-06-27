"""Embedding providers (swappable via ENV `EMBEDDING_PROVIDER`).

- `local`  : deterministic hashing embedding, no network/Azure required — runs locally.
- `azure_openai` : Azure OpenAI embeddings (requires a dedicated deployment).

LOCAL-FIRST: defaults to `local` so Phase 2 can run offline. Production should use Azure ada-002.
"""
from __future__ import annotations

import hashlib
import math
import re
from abc import ABC, abstractmethod

from app.core.config import get_settings

_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


class EmbeddingProvider(ABC):
    dim: int

    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...

    async def embed_many(self, texts: list[str]) -> list[list[float]]:
        return [await self.embed(t) for t in texts]


class LocalHashingEmbedding(EmbeddingProvider):
    """Bag-of-words hashing + L2 normalize. Sufficient for cosine retrieval in dev."""

    def __init__(self, dim: int = 256) -> None:
        self.dim = dim

    async def embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        tokens = _TOKEN_RE.findall(text.lower())
        for tok in tokens:
            h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dim
            sign = 1.0 if (h >> 8) % 2 == 0 else -1.0
            vec[idx] += sign
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]


class AzureOpenAIEmbedding(EmbeddingProvider):
    def __init__(self, dim: int = 1536) -> None:
        self.dim = dim
        settings = get_settings()
        from openai import AsyncOpenAI

        self._deployment = settings.azure_embed_deployment
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            default_query={"api-version": settings.openai_api_version},
        )

    async def embed(self, text: str) -> list[float]:
        resp = await self._client.embeddings.create(model=self._deployment, input=text)
        return resp.data[0].embedding


def get_embedding_provider() -> EmbeddingProvider:
    settings = get_settings()
    if settings.embedding_provider == "azure_openai" and settings.azure_embed_deployment:
        return AzureOpenAIEmbedding()
    return LocalHashingEmbedding()
