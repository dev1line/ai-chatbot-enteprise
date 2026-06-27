from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration. LOCAL-FIRST: runs locally by default without Azure."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=(),
    )

    # --- Run mode / flags ---
    app_env: Literal["local", "docker", "staging", "prod"] = "local"
    app_name: str = "AI Chatbot Enterprise"
    debug: bool = True

    # --- Providers (swappable via ENV) ---
    secrets_provider: Literal["env", "azure_key_vault"] = "env"
    llm_provider: Literal["mock", "azure_openai"] = "mock"
    embedding_provider: Literal["local", "azure_openai"] = "local"
    vector_db_provider: Literal["milvus", "qdrant", "pinecone", "memory"] = "memory"

    # --- Security ---
    jwt_secret: str = "dev-secret-change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # --- Database ---
    database_url: str = "postgresql://app:app@localhost:5432/app"

    # --- CORS ---
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # --- Vector DB ---
    qdrant_url: str = "http://qdrant:6333"

    # --- Azure OpenAI (used when llm_provider=azure_openai) ---
    # Supports Azure's "OpenAI v1 compatible" format: base_url .../openai/v1
    openai_api_key: str = ""
    openai_base_url: str = ""
    openai_api_type: str = "azure"
    openai_api_version: str = "2024-02-01"
    model_name: str = "gpt-5-mini"
    max_context_tokens: int = 2048
    completion_token_reserve: int = 256
    openai_verify_ssl: bool = True

    # Azure embeddings (optional, if a dedicated deployment is available)
    azure_embed_deployment: str = ""

    # --- RAG ---
    rag_top_k: int = 4
    rag_score_threshold: float = 0.0

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
