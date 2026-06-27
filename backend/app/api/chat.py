from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUserDep
from app.orchestration.llm import get_llm_provider
from app.repositories.conversation_repository import (
    ConversationRepository,
    MessageRepository,
)
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(payload: ChatRequest, current: CurrentUserDep) -> ChatResponse:
    conversations = ConversationRepository()
    messages = MessageRepository()

    if payload.conversation_id:
        conversation = await conversations.get(payload.conversation_id)
        if not conversation or conversation.userId != current.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")
    else:
        conversation = await conversations.create(
            user_id=current.id, title=payload.message[:60]
        )

    await messages.add(conversation.id, role="user", content=payload.message)

    result = await get_llm_provider().chat(payload.message, version=payload.version)

    citations_data = [c.model_dump() for c in result.citations]
    await messages.add(
        conversation.id,
        role="assistant",
        content=result.answer,
        citations=citations_data or None,
    )

    return ChatResponse(
        conversation_id=conversation.id,
        answer=result.answer,
        citations=result.citations,
    )
