from pydantic_settings import BaseSettings


class Config(BaseSettings):
    telegram_token: str
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = "anthropic/claude-3.5-sonnet"
    system_prompt: str = "Ты полезный ассистент."
    max_history_messages: int = 20
    temperature: float = 0.7
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

