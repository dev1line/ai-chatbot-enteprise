"""LLM provider abstraction (swappable qua ENV `LLM_PROVIDER`).

LOCAL-FIRST: mặc định `mock` để chạy local không cần Azure key.
Phase 2+ sẽ thay/RAG, Phase 7 trỏ Azure private VNet.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

import httpx
from fastapi import HTTPException, status
from openai import APIConnectionError, APIError, AsyncOpenAI, AuthenticationError

from app.core.config import Settings, get_settings
from app.schemas.chat import Citation


class LLMResult:
    def __init__(
        self,
        answer: str,
        citations: list[Citation] | None = None,
        usage: dict[str, int] | None = None,
    ) -> None:
        self.answer = answer
        self.citations = citations or []
        self.usage = usage or {}


class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, message: str, version: str | None = None) -> LLMResult: ...

    @abstractmethod
    async def complete(self, messages: Sequence[dict[str, str]]) -> LLMResult: ...


class MockLLM(LLMProvider):
    """Trả lời giả lập, dùng cho dev local & test. Chưa có RAG (Phase 2)."""

    async def chat(self, message: str, version: str | None = None) -> LLMResult:
        answer = (
            "[MOCK] Đã nhận câu hỏi: "
            f"'{message}'. RAG multimodal sẽ được nối ở Phase 2 "
            "(trả lời kèm citations từ kho tài liệu released)."
        )
        return LLMResult(answer=answer, citations=[])

    async def complete(self, messages: Sequence[dict[str, str]]) -> LLMResult:
        last_user_message = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user_message = msg.get("content", "")
                break
        answer = (
            "[MOCK] Đây là câu trả lời giả lập cho: "
            f"'{last_user_message}'. Hãy bật LLM_PROVIDER=azure_openai để gọi Azure OpenAI thật."
        )
        return LLMResult(
            answer=answer,
            citations=[],
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        )


class AzureOpenAILLM(LLMProvider):
    """Placeholder cho Azure OpenAI (bật khi LLM_PROVIDER=azure_openai).

    Triển khai gọi thật ở Phase 2 (RAG) / Phase 7 (private VNet).
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        api_key = self._resolve_api_key(settings)
        base_url = settings.openai_base_url or settings.azure_openai_endpoint
        self.model_name = settings.model_name or settings.azure_openai_deployment_chat
        if not api_key or not base_url or not self.model_name:
            raise ValueError(
                "Missing OpenAI config. Require OPENAI_API_KEY, OPENAI_BASE_URL and MODEL_NAME."
            )

        transport = httpx.AsyncHTTPTransport(retries=1, verify=settings.openai_verify_ssl)
        client_http = httpx.AsyncClient(transport=transport, timeout=30.0)
        default_query: dict[str, str] | None = None
        if "/openai/v1" not in base_url.rstrip("/"):
            default_query = {"api-version": settings.openai_api_version}

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            default_query=default_query,
            http_client=client_http,
        )

    @staticmethod
    def _resolve_api_key(settings: Settings) -> Any:
        if settings.openai_use_entra_id:
            try:
                from azure.identity import DefaultAzureCredential, get_bearer_token_provider
            except ImportError as exc:  # pragma: no cover
                raise ValueError(
                    "azure-identity is required when OPENAI_USE_ENTRA_ID=true"
                ) from exc
            return get_bearer_token_provider(
                DefaultAzureCredential(),
                settings.openai_entra_scope,
            )
        return settings.openai_api_key or settings.azure_openai_api_key

    async def chat(self, message: str, version: str | None = None) -> LLMResult:
        return await self.complete([{"role": "user", "content": message}])

    @staticmethod
    def _extract_chat_text(response: Any) -> str:
        if not getattr(response, "choices", None):
            return ""
        message = response.choices[0].message
        if not message:
            return ""

        content = message.content
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts: list[str] = []
            for part in content:
                if isinstance(part, dict):
                    text = part.get("text")
                    if isinstance(text, str) and text.strip():
                        parts.append(text.strip())
                else:
                    text = getattr(part, "text", None)
                    if isinstance(text, str) and text.strip():
                        parts.append(text.strip())
            return "\n".join(parts).strip()
        return ""

    async def _complete_via_responses(self, messages: Sequence[dict[str, str]]) -> LLMResult:
        input_items = [
            {"role": m.get("role", "user"), "content": m.get("content", "")}
            for m in messages
            if m.get("content", "").strip()
        ]

        response = await self.client.responses.create(
            model=self.model_name,
            input=input_items,
            max_output_tokens=self.settings.completion_token_reserve,
        )

        answer = (getattr(response, "output_text", "") or "").strip()
        if not answer:
            collected: list[str] = []
            output_items = getattr(response, "output", None) or []
            for item in output_items:
                content_parts = getattr(item, "content", None)
                if content_parts is None and isinstance(item, dict):
                    content_parts = item.get("content")
                if not content_parts:
                    continue
                for part in content_parts:
                    if isinstance(part, dict):
                        text = part.get("text")
                        if isinstance(text, str) and text.strip():
                            collected.append(text.strip())
                    else:
                        text = getattr(part, "text", None)
                        if isinstance(text, str) and text.strip():
                            collected.append(text.strip())
            answer = "\n".join(collected).strip()

        if not answer:
            answer = "Xin loi, hien tai toi khong lay duoc noi dung tra loi. Hay thu lai."
        usage_obj = getattr(response, "usage", None)
        usage = {
            "prompt_tokens": getattr(usage_obj, "input_tokens", 0) or 0,
            "completion_tokens": getattr(usage_obj, "output_tokens", 0) or 0,
            "total_tokens": getattr(usage_obj, "total_tokens", 0) or 0,
        }
        return LLMResult(answer=answer, citations=[], usage=usage)

    async def complete(self, messages: Sequence[dict[str, str]]) -> LLMResult:
        payload: dict[str, object] = {
            "model": self.model_name,
            "messages": list(messages),
        }
        if self.model_name.startswith("gpt-5") or self.model_name.startswith("o"):
            payload["max_completion_tokens"] = self.settings.completion_token_reserve
        else:
            payload["max_tokens"] = self.settings.completion_token_reserve

        try:
            response = await self.client.chat.completions.create(**payload)
        except AuthenticationError as exc:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                f"OpenAI authentication failed: {exc.message}",
            ) from exc
        except APIConnectionError as exc:
            raise HTTPException(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "OpenAI connection failed. Check OPENAI_BASE_URL/proxy/TLS settings.",
            ) from exc
        except APIError as exc:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY,
                f"OpenAI request failed: {exc.message}",
            ) from exc

        content = self._extract_chat_text(response)

        usage: dict[str, int] = {}
        if response.usage is not None:
            usage = {
                "prompt_tokens": response.usage.prompt_tokens or 0,
                "completion_tokens": response.usage.completion_tokens or 0,
                "total_tokens": response.usage.total_tokens or 0,
            }

        if not content:
            try:
                return await self._complete_via_responses(messages)
            except APIError:
                # Keep original behavior if fallback fails.
                pass

        return LLMResult(answer=content, citations=[], usage=usage)


def get_llm_provider() -> LLMProvider:
    settings = get_settings()
    if settings.llm_provider == "azure_openai":
        return AzureOpenAILLM(settings)
    return MockLLM()
