from pydantic_settings import BaseSettings
from pydantic import SecretStr, Field

class Settings(BaseSettings):
    openai_api_key: SecretStr
    model_name: str ="gpt-4o-mini"
    temperature: float = Field(default = 0.7, ge=0.0, le=2.0)
    max_tokens: int = 1000
    agent_name: str ="simple_agent"
    db_path: str = "agent_memory.db"

    class Config():
        env_file = ".env"

settings = Settings()
