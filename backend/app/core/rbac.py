from fastapi import Depends, HTTPException, status

from app.core.deps import get_current_user
from app.schemas.auth import CurrentUser

ROLE_RANK = {"VIEWER": 1, "ENGINEER": 2, "ADMIN": 3}


def require_role(min_role: str):
    """Dependency factory: require the user to have a role >= min_role.

    Designed to be reused at the tool/action layer (Phase 3) — every action checks the user's scope.
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
