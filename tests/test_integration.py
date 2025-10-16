"""Интеграционные тесты для полного цикла работы"""

import random
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.config import Config, load_system_prompt_with_fallback
from src.conversation import ConversationManager
from src.llm_client import LLMClient
from src.models import ChatMessage, ConversationKey


@pytest.fixture
def config() -> Config:
    return Config(
        telegram_token="test",
        openrouter_api_key="test",
        system_prompt="You are helpful assistant",
        max_history_messages=3,
    )


@pytest.fixture
def llm_client(config: Config) -> LLMClient:
    return LLMClient(config)


@pytest.mark.asyncio
async def test_full_conversation_cycle(
    config: Config, conversation_manager: ConversationManager, llm_client: LLMClient
) -> None:
    """Полный цикл: user message → LLM → response → history"""
    test_id = random.randint(100000, 999999)
    key = ConversationKey(chat_id=test_id, user_id=test_id)

    # Очищаем историю перед тестом для гарантии чистого начала
    await conversation_manager.clear_history(key)

    # Mock LLM response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello! How can I help you?"

    with patch.object(
        llm_client.client.chat.completions, "create", new=AsyncMock(return_value=mock_response)
    ):
        # User sends message
        user_msg = ChatMessage(role="user", content="Hello")
        await conversation_manager.add_message(key, user_msg)

        # Get history with system prompt
        history = await conversation_manager.get_history(key, config.system_prompt)

        # LLM processes
        response = await llm_client.get_response(history)

        # Add assistant response to history
        assistant_msg = ChatMessage(role="assistant", content=response)
        await conversation_manager.add_message(key, assistant_msg)

        # Check final history
        final_history = await conversation_manager.get_history(key, config.system_prompt)

        expected_length = 3  # system + user + assistant
        assert len(final_history) == expected_length
        assert final_history[0].role == "system"
        assert final_history[1].content == "Hello"
        assert final_history[2].content == "Hello! How can I help you?"


@pytest.mark.asyncio
async def test_conversation_with_context(
    config: Config, conversation_manager: ConversationManager, llm_client: LLMClient
) -> None:
    """LLM должен получать контекст предыдущих сообщений"""
    key = ConversationKey(chat_id=1, user_id=1)

    # Add previous messages
    await conversation_manager.add_message(
        key, ChatMessage(role="user", content="My name is Pavel")
    )
    await conversation_manager.add_message(
        key, ChatMessage(role="assistant", content="Nice to meet you, Pavel!")
    )

    # New message
    await conversation_manager.add_message(
        key, ChatMessage(role="user", content="What is my name?")
    )

    history = await conversation_manager.get_history(key, config.system_prompt)

    # Should contain all previous messages
    expected_length = 4  # system + 3 messages
    assert len(history) == expected_length
    assert any("Pavel" in msg.content for msg in history)


@pytest.mark.asyncio
async def test_clear_context(config: Config, conversation_manager: ConversationManager) -> None:
    """После clear история должна быть пустой"""
    key = ConversationKey(chat_id=1, user_id=1)

    # Add messages
    await conversation_manager.add_message(key, ChatMessage(role="user", content="Test 1"))
    await conversation_manager.add_message(key, ChatMessage(role="assistant", content="Response 1"))

    # Clear
    await conversation_manager.clear_history(key)

    # New history should only have system prompt
    history = await conversation_manager.get_history(key, config.system_prompt)
    assert len(history) == 1
    assert history[0].role == "system"


@pytest.mark.asyncio
async def test_history_limit_integration(
    config: Config, conversation_manager: ConversationManager
) -> None:
    """Интеграционный тест ограничения истории"""
    key = ConversationKey(chat_id=1, user_id=1)

    # Simulate conversation: add more messages than limit
    for i in range(5):
        await conversation_manager.add_message(
            key, ChatMessage(role="user", content=f"Question {i}")
        )
        await conversation_manager.add_message(
            key, ChatMessage(role="assistant", content=f"Answer {i}")
        )

    history = await conversation_manager.get_history(key, config.system_prompt)

    # Should keep system + max_history_messages (3)
    # But we added 10 messages (5 pairs), so should keep last 3
    expected_length = 4  # system + 3 messages
    assert len(history) == expected_length
    assert history[0].role == "system"

    # Check that old messages were removed
    assert "Question 0" not in str([msg.content for msg in history])
    assert "Question 4" in str([msg.content for msg in history])


def test_load_system_prompt_on_startup(tmp_path: Path) -> None:
    """Тест загрузки системного промпта из файла при старте бота"""
    # Создать временный файл промпта
    prompt_file = tmp_path / "system.txt"
    prompt_file.write_text("Ты специализированный ассистент.", encoding="utf-8")

    # Загрузить промпт
    prompt = load_system_prompt_with_fallback(str(prompt_file))

    # Проверить
    assert prompt == "Ты специализированный ассистент."


def test_load_system_prompt_fallback() -> None:
    """Тест fallback на дефолтный промпт при отсутствии файла"""
    # Попытаться загрузить несуществующий файл
    prompt = load_system_prompt_with_fallback("nonexistent_file.txt")

    # Проверить дефолтное значение
    assert prompt == "Ты полезный ассистент."
