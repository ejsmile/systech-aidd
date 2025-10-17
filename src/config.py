import logging

from pydantic import model_validator
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
    database_url: str = "postgresql+asyncpg://aidd_user:aidd_password@localhost:5432/aidd_db"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    model_name: str = "openai/gpt-oss-20b:free"
    system_prompt_file: str = "prompts/system.txt"  # Путь к файлу с системным промптом
    system_prompt: str = ""  # Будет заполнено в model_validator
    max_history_messages: int = 20
    temperature: float = 0.7
    log_level: str = "INFO"
    _skip_prompt_loading: bool = False  # Флаг для пропуска загрузки промпта из файла

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def load_system_prompt_from_file(self) -> "Config":
        """Загрузить системный промпт из файла после инициализации."""
        # Skip loading from file if explicitly told to skip
        if self._skip_prompt_loading:
            # If system_prompt is empty, use default
            if not self.system_prompt:
                self.system_prompt = DEFAULT_SYSTEM_PROMPT
        else:
            # Load from file if system_prompt is still default or empty
            if not self.system_prompt or self.system_prompt == DEFAULT_SYSTEM_PROMPT:
                self.system_prompt = load_system_prompt_with_fallback(self.system_prompt_file)
            # Ensure system_prompt is never empty
            if not self.system_prompt:
                self.system_prompt = DEFAULT_SYSTEM_PROMPT
        return self
