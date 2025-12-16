from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Base URLs
    ollama_url: str = "http://localhost:11434"

    # Timeouts
    http_timeout_s: int = 120

    # Router defaults
    default_provider: str = "ollama"

    model_config = SettingsConfigDict(env_prefix="LLM_", env_file=".env", extra="ignore")

settings = Settings()
