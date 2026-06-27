from typing import Any

from app.core.db import get_db


class ConversationRepository:
    async def create(self, user_id: str, title: str | None = None) -> Any:
        return await get_db().conversation.create(
            data={"title": title, "user": {"connect": {"id": user_id}}}
        )

    async def get(self, conversation_id: str) -> Any | None:
        return await get_db().conversation.find_unique(where={"id": conversation_id})

    async def list_by_user(self, user_id: str, skip: int = 0, take: int = 20) -> list[Any]:
        return await get_db().conversation.find_many(
            where={"userId": user_id},
            order={"createdAt": "desc"},
            skip=skip,
            take=take,
        )


class MessageRepository:
    async def add(
        self,
        conversation_id: str,
        role: str,
        content: str,
        citations: Any | None = None,
    ) -> Any:
        data: dict[str, Any] = {
            "role": role,
            "content": content,
            "conversation": {"connect": {"id": conversation_id}},
        }
        if citations is not None:
            data["citations"] = citations
        return await get_db().message.create(data=data)

    async def list_for_conversation(self, conversation_id: str) -> list[Any]:
        return await get_db().message.find_many(
            where={"conversationId": conversation_id},
            order={"createdAt": "asc"},
        )

    async def list_paginated(
        self,
        conversation_id: str,
        skip: int = 0,
        take: int = 20,
    ) -> list[Any]:
        return await get_db().message.find_many(
            where={"conversationId": conversation_id},
            order={"createdAt": "asc"},
            skip=skip,
            take=take,
        )

    async def list_for_context(self, conversation_id: str, take: int = 30) -> list[Any]:
        rows = await get_db().message.find_many(
            where={"conversationId": conversation_id},
            order={"createdAt": "desc"},
            take=take,
        )
        rows.reverse()
        return rows
