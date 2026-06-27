from fastapi import APIRouter, HTTPException, status

from app.core.deps import CurrentUserDep
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])

_VALID_ROLES = {"ADMIN", "ENGINEER", "VIEWER"}


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest) -> TokenResponse:
    if payload.role not in _VALID_ROLES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid role")
    repo = UserRepository()
    if await repo.get_by_email(payload.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    user = await repo.create(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        role=payload.role,
    )
    token = create_access_token(subject=user.id, role=user.role)
    return TokenResponse(access_token=token, role=user.role)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    repo = UserRepository()
    user = await repo.get_by_email(payload.email)
    if not user or not verify_password(payload.password, user.hashedPassword):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    token = create_access_token(subject=user.id, role=user.role)
    return TokenResponse(access_token=token, role=user.role)


@router.get("/me", response_model=UserResponse)
async def me(current: CurrentUserDep) -> UserResponse:
    user = await UserRepository().get_by_id(current.id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return UserResponse(
        id=user.id, email=user.email, full_name=user.fullName, role=user.role
    )
