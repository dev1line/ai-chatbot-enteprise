from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.schemas.auth import CurrentUser

_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token") from None
    user_id = payload.get("sub")
    role = payload.get("role", "VIEWER")
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token payload")
    return CurrentUser(id=user_id, role=role)


CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]
