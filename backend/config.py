"""
Application configuration management.
Loads from environment variables with sensible defaults.
Uses Pydantic v2 Settings for validation and type safety.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration with environment variable support.
    All environment variables are case-insensitive.
    """

    # Core
    environment: str = Field(default="development", description="Environment name")
    debug: bool = Field(default=True, description="Enable debug mode")
    version: str = Field(default="0.1.0", description="Application version")
    app_name: str = Field(default="GenAI Governance Platform", description="Application name")

    # Database (auto-detects: SQLite for local dev, Postgres for production)
    database_url: str = Field(
        default="sqlite:///genai_governance.db",  # Local SQLite for no-Docker development
        description="Database URL (SQLite for local, PostgreSQL for production)"
    )

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL"
    )

    # Security
    secret_key: str = Field(
        default="dev-secret-key-change-in-production-must-be-32-chars-min",
        description="Secret key for JWT signing (min 32 chars in production)"
    )
    algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=30, description="JWT token expiration")

    # FastAPI
    backend_host: str = Field(default="0.0.0.0", description="Backend bind host")
    backend_port: int = Field(default=8000, description="Backend bind port")

    # LLM Configuration
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(
        default="gpt-4-turbo-preview",
        description="OpenAI model to use"
    )
    embedding_model: str = Field(
        default="text-embedding-3-large",
        description="Embedding model for RAG"
    )
    use_local_llm: bool = Field(default=False, description="Use local LLM instead of OpenAI")
    local_llm_url: str = Field(
        default="http://localhost:11434",
        description="Local LLM endpoint (e.g., Ollama)"
    )
    local_embedding_model: str = Field(
        default="all-minilm-l6-v2",
        description="Local embedding model"
    )
    nli_model: str = Field(
        default="roberta-large-mnli",
        description="NLI model for entailment verification"
    )

    # Governance Settings
    log_retention_days: int = Field(default=90, description="Log retention period in days")
    pseudonym_rotation_days: int = Field(default=30, description="Pseudonym rotation period")
    enable_detailed_traces: bool = Field(
        default=True,
        description="Enable detailed governance decision traces"
    )

    # Transparency
    student_visible_logs: bool = Field(default=True, description="Show logs to students")
    show_policy_links: bool = Field(default=True, description="Show policy links in UI")

    # Contact
    admin_email: str = Field(default="admin@institution.edu", description="Admin email")
    support_email: str = Field(
        default="ai-governance@institution.edu",
        description="Support email"
    )

    model_config = {
        "env_file": ".env.local",
        "case_sensitive": False,
        "validate_default": True,
    }


# Global settings instance
settings = Settings()
