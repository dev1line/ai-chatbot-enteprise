from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    full_name: str | None = None
    role: str = "VIEWER"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    role: str


class CurrentUser(BaseModel):
    id: str
    role: str
