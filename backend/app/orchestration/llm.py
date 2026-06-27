"""LLM provider abstraction (swappable via ENV `LLM_PROVIDER`).

- `mock`         : mocked responses (local, Azure not required).
- `azure_openai` : Azure OpenAI (OpenAI v1 format: base_url .../openai/v1).

LOCAL-FIRST: defaults to `mock`. Set LLM_PROVIDER=azure_openai + OPENAI_* to use real Azure.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import Settings, get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def _transient_errors() -> tuple[type[Exception], ...]:
    """Only retry transient errors (network/timeout/rate-limit), do NOT retry 400."""
    import openai

    return (
        openai.APIConnectionError,
        openai.APITimeoutError,
        openai.RateLimitError,
        openai.InternalServerError,
    )


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, system: str, user: str) -> str: ...


class MockLLM(LLMProvider):
    async def generate(self, system: str, user: str) -> str:
        return (
            "[MOCK] (Azure not enabled) This is a mocked answer based on the retrieved context. "
            "Set LLM_PROVIDER=azure_openai to use a real model."
        )


class AzureOpenAILLM(LLMProvider):
    def __init__(self, settings: Settings) -> None:
        from openai import AsyncOpenAI

        self.settings = settings
        self._client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            default_query={"api-version": settings.openai_api_version},
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        retry=retry_if_exception_type(_transient_errors()),
        reraise=True,
    )
    async def generate(self, system: str, user: str) -> str:
        resp = await self._client.chat.completions.create(
            model=self.settings.model_name,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_completion_tokens=self.settings.completion_token_reserve
            + self.settings.max_context_tokens,
        )
        return resp.choices[0].message.content or ""


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    if settings.llm_provider == "azure_openai" and settings.openai_api_key:
        logger.info("Using AzureOpenAILLM (model=%s)", settings.model_name)
        return AzureOpenAILLM(settings)
    return MockLLM()
