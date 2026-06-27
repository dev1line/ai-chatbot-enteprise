from typing import Any

from app.core.db import get_db


class UserRepository:
    """Cô lập mọi truy vấn User. Router KHÔNG được gọi Prisma trực tiếp."""

    async def get_by_email(self, email: str) -> Any | None:
        return await get_db().user.find_unique(where={"email": email})

    async def get_by_id(self, user_id: str) -> Any | None:
        return await get_db().user.find_unique(where={"id": user_id})

    async def create(
        self, email: str, hashed_password: str, full_name: str | None, role: str
    ) -> Any:
        return await get_db().user.create(
            data={
                "email": email,
                "hashedPassword": hashed_password,
                "fullName": full_name,
                "role": role,
            }
        )
