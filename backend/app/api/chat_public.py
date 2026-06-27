from fastapi import APIRouter, HTTPException, status

from app.core.config import get_settings
from app.orchestration.context import trim_messages_to_budget
from app.orchestration.llm import get_llm_provider
from app.schemas.chat import CompletionUsage, PublicCompletionRequest, PublicCompletionResponse

router = APIRouter(prefix="/api/public/chat", tags=["chat-public"])


@router.post("/completions", response_model=PublicCompletionResponse)
async def create_public_completion(payload: PublicCompletionRequest) -> PublicCompletionResponse:
    settings = get_settings()
    messages = [{"role": turn.role, "content": turn.content} for turn in payload.history]
    messages.append({"role": "user", "content": payload.message})

    trimmed = trim_messages_to_budget(
        messages,
        max_context_tokens=settings.max_context_tokens,
        completion_token_reserve=settings.completion_token_reserve,
    )

    try:
        result = await get_llm_provider().complete(trimmed)
    except ValueError as exc:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "LLM provider is not configured. Set OPENAI_API_KEY, OPENAI_BASE_URL, MODEL_NAME.",
        ) from exc

    return PublicCompletionResponse(
        answer=result.answer,
        usage=CompletionUsage(**result.usage),
    )
