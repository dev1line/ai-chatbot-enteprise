from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Cấu hình ứng dụng. LOCAL-FIRST: mặc định chạy được local không cần Azure."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Run mode / flags ---
    app_env: Literal["local", "docker", "staging", "prod"] = "local"
    app_name: str = "AI Chatbot Enterprise"
    debug: bool = True

    # --- Providers (swappable qua ENV) ---
    secrets_provider: Literal["env", "azure_key_vault"] = "env"
    llm_provider: Literal["mock", "azure_openai"] = "mock"
    embedding_provider: Literal["mock", "azure_openai"] = "mock"
    vector_db_provider: Literal["milvus", "qdrant", "pinecone", "memory"] = "memory"

    # --- Security ---
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- Database ---
    database_url: str = "postgresql://app:app@localhost:5432/app"

    # --- CORS ---
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # --- Azure (chỉ dùng khi llm_provider=azure_openai) ---
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_deployment_chat: str = ""
    azure_openai_deployment_embed: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
