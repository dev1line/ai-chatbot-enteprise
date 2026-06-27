from typing import Any

from app.core.db import get_db


class DocumentRepository:
    """Immutable document repository metadata (version + content_hash)."""

    async def upsert_metadata(
        self,
        doc_id: str,
        version: str,
        source: str,
        doc_type: str,
        content_hash: str | None,
        metadata: dict[str, Any] | None = None,
    ) -> Any:
        from prisma import Json

        meta_json = Json(metadata) if metadata is not None else Json({})
        return await get_db().document.upsert(
            where={"docId_version": {"docId": doc_id, "version": version}},
            data={
                "create": {
                    "docId": doc_id,
                    "version": version,
                    "source": source,
                    "type": doc_type,
                    "contentHash": content_hash,
                    "metadata": meta_json,
                },
                "update": {
                    "source": source,
                    "type": doc_type,
                    "contentHash": content_hash,
                    "metadata": meta_json,
                },
            },
        )

    async def list_all(self) -> list[Any]:
        return await get_db().document.find_many(order={"releasedAt": "desc"})
