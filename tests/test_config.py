"""Тесты для валидации конфигурации"""

from pathlib import Path

from src.config import Config, load_system_prompt, load_system_prompt_with_fallback
from tests.conftest import ConfigForTests

# Default values from Config
DEFAULT_MAX_HISTORY = 20
DEFAULT_TEMPERATURE = 0.7
CUSTOM_MAX_HISTORY = 10
CUSTOM_TEMPERATURE = 0.5


def test_config_with_required_fields() -> None:
    """Конфигурация с обязательными полями"""
    config = ConfigForTests(
        telegram_token="test_token",
        openrouter_api_key="test_key",
    )

    assert config.telegram_token == "test_token"
    assert config.openrouter_api_key == "test_key"
    assert config.model_name == "openai/gpt-oss-20b:free"  # default
    assert config.max_history_messages == DEFAULT_MAX_HISTORY


def test_config_with_custom_values() -> None:
    """Конфигурация с кастомными значениями"""
    config = ConfigForTests(
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


def test_config_test_defaults() -> None:
    """Проверка что другие дефолтные значения правильные"""
    config = ConfigForTests(
        telegram_token="test",
        openrouter_api_key="test",
        system_prompt="Custom test prompt",
    )

    assert config.openrouter_base_url == "https://openrouter.ai/api/v1"
    assert config.model_name == "openai/gpt-oss-20b:free"
    assert config.system_prompt == "Custom test prompt"  # Use provided value
    assert config.max_history_messages == DEFAULT_MAX_HISTORY
    assert config.temperature == DEFAULT_TEMPERATURE
    assert config.log_level == "INFO"


def test_load_system_prompt_from_file(tmp_path: Path) -> None:
    """Тест загрузки системного промпта из файла."""
    # Создать временный файл с промптом
    prompt_file = tmp_path / "prompt.txt"
    prompt_file.write_text("Ты тестовый ассистент.", encoding="utf-8")

    # Загрузить промпт
    prompt = load_system_prompt(str(prompt_file))

    # Проверить
    assert prompt == "Ты тестовый ассистент."


def test_load_system_prompt_fallback_on_missing_file() -> None:
    """Тест fallback на дефолтный промпт при отсутствии файла."""
    # Попытаться загрузить несуществующий файл
    prompt = load_system_prompt_with_fallback("nonexistent.txt")

    # Проверить дефолтное значение
    assert prompt == "Ты полезный ассистент."


def test_config_system_prompt_file_default() -> None:
    """Тест дефолтного значения system_prompt_file в конфиге."""
    config = Config(telegram_token="test_token", openrouter_api_key="test_key")
    assert config.system_prompt_file == "prompts/system.txt"
