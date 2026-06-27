from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from app.core.config import get_settings
from app.core.deps import CurrentUserDep
from app.orchestration.context import trim_messages_to_budget
from app.orchestration.llm import get_llm_provider
from app.repositories.conversation_repository import ConversationRepository, MessageRepository
from app.schemas.chat import (
    CompletionRequest,
    CompletionResponse,
    CompletionUsage,
    MessageListResponse,
    MessageResponse,
    SessionListResponse,
    SessionResponse,
)

router = APIRouter(prefix="/api/v1/chat", tags=["chat-v1"])


@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    current: CurrentUserDep,
    title: str | None = None,
) -> SessionResponse:
    conversation = await ConversationRepository().create(user_id=current.id, title=title)
    return SessionResponse(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.createdAt.isoformat(),
    )


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(current: CurrentUserDep) -> SessionListResponse:
    items = await ConversationRepository().list_by_user(current.id)
    return SessionListResponse(
        items=[
            SessionResponse(
                id=row.id,
                title=row.title,
                created_at=row.createdAt.isoformat(),
            )
            for row in items
        ]
    )


@router.get("/sessions/{session_id}/messages", response_model=MessageListResponse)
async def list_messages(
    session_id: str,
    current: CurrentUserDep,
    page: int = Query(1, ge=1),
    page_size: int | None = Query(None, ge=1, le=100),
) -> MessageListResponse:
    conversation = await ConversationRepository().get(session_id)
    if not conversation or conversation.userId != current.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

    settings = get_settings()
    final_page_size = page_size or settings.default_page_size
    skip = (page - 1) * final_page_size

    rows = await MessageRepository().list_paginated(
        conversation_id=session_id,
        skip=skip,
        take=final_page_size,
    )

    return MessageListResponse(
        items=[
            MessageResponse(
                id=row.id,
                role=row.role,
                content=row.content,
                created_at=row.createdAt.isoformat(),
            )
            for row in rows
        ],
        page=page,
        page_size=final_page_size,
    )


@router.post("/completions", response_model=CompletionResponse)
async def create_completion(
    payload: CompletionRequest,
    current: CurrentUserDep,
) -> CompletionResponse:
    conversation = await ConversationRepository().get(payload.session_id)
    if not conversation or conversation.userId != current.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Session not found")

    messages_repo = MessageRepository()
    await messages_repo.add(payload.session_id, role="user", content=payload.content)

    history = await messages_repo.list_for_context(payload.session_id)
    raw_messages = [{"role": row.role, "content": row.content} for row in history]

    settings = get_settings()
    trimmed = trim_messages_to_budget(
        raw_messages,
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

    await messages_repo.add(
        payload.session_id,
        role="assistant",
        content=result.answer,
        citations=[c.model_dump() for c in result.citations] or None,
    )

    usage = CompletionUsage(**result.usage)
    return CompletionResponse(
        session_id=payload.session_id,
        assistant_message=result.answer,
        usage=usage,
    )
