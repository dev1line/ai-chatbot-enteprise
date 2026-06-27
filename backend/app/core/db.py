"""Prisma client lifecycle.

Lazy import so that tests not requiring a DB (health, auth) can run without needing
`prisma generate`. The real client is created at app startup (in Docker it has already
been generated + db pushed).
"""
from typing import Any

from app.core.logging import get_logger

logger = get_logger(__name__)

_client: Any | None = None


async def connect_db() -> None:
    global _client
    if _client is not None:
        return
    from prisma import Prisma  # lazy import

    _client = Prisma()
    await _client.connect()
    logger.info("Prisma connected")


async def disconnect_db() -> None:
    global _client
    if _client is not None:
        await _client.disconnect()
        _client = None
        logger.info("Prisma disconnected")


def get_db() -> Any:
    if _client is None:
        raise RuntimeError("Database not connected. Call connect_db() on startup.")
    return _client
