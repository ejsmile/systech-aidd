"""Общие fixtures для тестов"""

import pytest

from src.config import Config
from src.conversation import ConversationManager


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
