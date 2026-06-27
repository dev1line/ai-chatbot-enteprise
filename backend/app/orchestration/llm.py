"""LLM provider abstraction (swappable qua ENV `LLM_PROVIDER`).

LOCAL-FIRST: mặc định `mock` để chạy local không cần Azure key.
Phase 2+ sẽ thay/RAG, Phase 7 trỏ Azure private VNet.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from app.core.config import Settings, get_settings
from app.schemas.chat import Citation


class LLMResult:
    def __init__(self, answer: str, citations: list[Citation] | None = None) -> None:
        self.answer = answer
        self.citations = citations or []


class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, message: str, version: str | None = None) -> LLMResult: ...


class MockLLM(LLMProvider):
    """Trả lời giả lập, dùng cho dev local & test. Chưa có RAG (Phase 2)."""

    async def chat(self, message: str, version: str | None = None) -> LLMResult:
        answer = (
            "[MOCK] Đã nhận câu hỏi: "
            f"'{message}'. RAG multimodal sẽ được nối ở Phase 2 "
            "(trả lời kèm citations từ kho tài liệu released)."
        )
        return LLMResult(answer=answer, citations=[])


class AzureOpenAILLM(LLMProvider):
    """Placeholder cho Azure OpenAI (bật khi LLM_PROVIDER=azure_openai).

    Triển khai gọi thật ở Phase 2 (RAG) / Phase 7 (private VNet).
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def chat(self, message: str, version: str | None = None) -> LLMResult:
        raise NotImplementedError(
            "AzureOpenAILLM sẽ được hiện thực ở Phase 2. Dùng LLM_PROVIDER=mock cho local."
        )


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    if settings.llm_provider == "azure_openai":
        return AzureOpenAILLM(settings)
    return MockLLM()
