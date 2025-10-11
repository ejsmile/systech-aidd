"""Общие fixtures для тестов"""

import pytest
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource

from src.config import Config
from src.conversation import ConversationManager


class ConfigForTests(Config):
    """Config для тестов - без загрузки .env файла и переменных окружения"""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Используем только параметры инициализации, игнорируем .env и env переменные
        return (init_settings,)


@pytest.fixture
def mock_config() -> Config:
    """Минимальная валидная конфигурация для тестов"""
    return Config(
        telegram_token="test_token_123",
        openrouter_api_key="test_api_key_123",
    )


@pytest.fixture
def conversation_manager() -> ConversationManager:
    """ConversationManager с настройками для тестов"""
    return ConversationManager(max_history_messages=3)
