"""Тесты для валидации конфигурации"""

from src.config import Config

# Default values from Config
DEFAULT_MAX_HISTORY = 20
DEFAULT_TEMPERATURE = 0.7
CUSTOM_MAX_HISTORY = 10
CUSTOM_TEMPERATURE = 0.5


def test_config_with_required_fields() -> None:
    """Конфигурация с обязательными полями"""
    config = Config(
        telegram_token="test_token",
        openrouter_api_key="test_key",
        _env_file=None,  # Отключаем загрузку .env для тестов
    )

    assert config.telegram_token == "test_token"
    assert config.openrouter_api_key == "test_key"
    assert config.model_name == "openai/gpt-oss-20b:free"  # default
    assert config.max_history_messages == DEFAULT_MAX_HISTORY


def test_config_with_custom_values() -> None:
    """Конфигурация с кастомными значениями"""
    config = Config(
        telegram_token="test",
        openrouter_api_key="test",
        model_name="gpt-4",
        temperature=CUSTOM_TEMPERATURE,
        max_history_messages=CUSTOM_MAX_HISTORY,
        system_prompt="Custom prompt",
    )

    assert config.model_name == "gpt-4"
    assert config.temperature == CUSTOM_TEMPERATURE
    assert config.max_history_messages == CUSTOM_MAX_HISTORY
    assert config.system_prompt == "Custom prompt"


def test_config_default_values() -> None:
    """Проверка значений по умолчанию"""
    config = Config(
        telegram_token="test",
        openrouter_api_key="test",
        _env_file=None,  # Отключаем загрузку .env для тестов
    )

    assert config.openrouter_base_url == "https://openrouter.ai/api/v1"
    assert config.model_name == "openai/gpt-oss-20b:free"
    assert config.system_prompt == "Ты полезный ассистент."
    assert config.max_history_messages == DEFAULT_MAX_HISTORY
    assert config.temperature == DEFAULT_TEMPERATURE
    assert config.log_level == "INFO"
