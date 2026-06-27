from fastapi import Depends, HTTPException, status

from app.core.deps import get_current_user
from app.schemas.auth import CurrentUser

ROLE_RANK = {"VIEWER": 1, "ENGINEER": 2, "ADMIN": 3}


def require_role(min_role: str):
    """Dependency factory: yêu cầu user có vai trò >= min_role.

    Thiết kế để tái dùng ở tầng tool/action (Phase 3) — mọi action kiểm tra scope user.
    """
    required_rank = ROLE_RANK[min_role]

    async def _checker(user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if ROLE_RANK.get(user.role, 0) < required_rank:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                f"Requires role >= {min_role}",
            )
        return user

    return _checker
