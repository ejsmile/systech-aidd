import logging

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = "Ты полезный ассистент."


def load_system_prompt(file_path: str) -> str:
    """Загрузить системный промпт из файла."""
    with open(file_path, encoding="utf-8") as f:
        return f.read().strip()


def load_system_prompt_with_fallback(file_path: str) -> str:
    """Загрузить системный промпт с fallback на дефолт."""
    try:
        return load_system_prompt(file_path)
    except FileNotFoundError:
        logger.warning(f"Файл промпта не найден: {file_path}, используется дефолтный промпт")
        return DEFAULT_SYSTEM_PROMPT


class Config(BaseSettings):
    telegram_token: str
    openrouter_api_key: str
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = "openai/gpt-oss-20b:free"
    system_prompt: str = "Ты полезный ассистент."
    system_prompt_file: str = "prompts/system.txt"  # Путь к файлу с системным промптом
    max_history_messages: int = 20
    temperature: float = 0.7
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
