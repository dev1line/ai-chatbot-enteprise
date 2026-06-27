"""LLM provider unit tests (mock + Azure OpenAI with mocked client)."""
from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.core.config import Settings, get_settings
from app.orchestration.llm import (
    AzureOpenAILLM,
    MockLLM,
    _synthesize_from_context,
    get_llm_provider,
)


def test_synthesize_from_context_extracts_answer():
    user = (
        "CONTEXT:\n"
        "[1] (doc=SEC-1 v=v2.1) KMS keys rotate every 90 days.\n\n"
        "QUESTION: How often are keys rotated?\n\n"
        "Answer (with references [number]):"
    )
    result = _synthesize_from_context(user)
    assert result is not None
    assert "90 days" in result
    assert "[1]" in result


@pytest.mark.asyncio
async def test_mock_llm_uses_context():
    llm = MockLLM()
    user = (
        "CONTEXT:\n"
        "[1] (doc=OPS v=v1) Restart payment-service using rollout.\n\n"
        "QUESTION: How to restart payment service?\n\n"
        "Answer (with references [number]):"
    )
    answer = await llm.generate("system", user)
    assert "payment-service" in answer.lower() or "restart" in answer.lower()
    assert "[MOCK]" not in answer


@pytest.mark.asyncio
async def test_mock_llm_fallback_without_context():
    llm = MockLLM()
    answer = await llm.generate("system", "plain question")
    assert "[MOCK]" in answer


@pytest.mark.asyncio
async def test_azure_openai_llm_generate(monkeypatch):
    mock_message = MagicMock()
    mock_message.content = "KMS keys must be rotated every 90 days per policy."
    mock_choice = MagicMock()
    mock_choice.message = mock_message
    mock_resp = MagicMock()
    mock_resp.choices = [mock_choice]

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_resp)

    settings = Settings(
        llm_provider="azure_openai",
        openai_api_key="test-key",
        openai_base_url="https://test.openai.azure.com/openai/v1",
        model_name="gpt-4o-mini",
    )
    llm = AzureOpenAILLM(settings)
    llm._client = mock_client

    answer = await llm.generate(
        "You are an assistant.",
        "CONTEXT:\nKMS rotation 90 days\n\nQUESTION: rotation schedule?",
    )
    assert "90 days" in answer
    mock_client.chat.completions.create.assert_awaited_once()
    call_kwargs = mock_client.chat.completions.create.await_args.kwargs
    assert call_kwargs["model"] == "gpt-4o-mini"
    assert call_kwargs["messages"][0]["role"] == "system"


def test_get_llm_provider_selects_mock_by_default(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    get_settings.cache_clear()
    provider = get_llm_provider()
    assert isinstance(provider, MockLLM)
    get_settings.cache_clear()


def test_get_llm_provider_selects_azure_when_configured(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "azure_openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://test.openai.azure.com/openai/v1")
    get_settings.cache_clear()
    provider = get_llm_provider()
    assert isinstance(provider, AzureOpenAILLM)
    get_settings.cache_clear()
