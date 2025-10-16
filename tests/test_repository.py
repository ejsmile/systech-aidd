"""Тесты для repository.py"""

from typing import TYPE_CHECKING

import pytest

from src.models import ChatMessage, ConversationKey
from src.repository import MessageRepository

if TYPE_CHECKING:
    from src.conversation import ConversationManager


@pytest.mark.asyncio
async def test_repository_get_history_count(
    db_session, conversation_manager: "ConversationManager"
) -> None:
    """Тест получения количества сообщений в диалоге"""
    key = ConversationKey(chat_id=9001, user_id=9001)

    # Добавляем несколько сообщений
    await conversation_manager.add_message(key, ChatMessage(role="user", content="Message 1"))
    await conversation_manager.add_message(key, ChatMessage(role="assistant", content="Response 1"))
    await conversation_manager.add_message(key, ChatMessage(role="user", content="Message 2"))

    # Получаем количество
    repo = MessageRepository(db_session)
    count = await repo.get_history_count(key)

    # Ожидаем 4 сообщения: system (добавлен при первом get_history) + 3 добавленных
    # Но так как мы не вызывали get_history, system prompt не добавлен
    assert count == 3  # noqa: PLR2004


@pytest.mark.asyncio
async def test_repository_soft_delete_returns_count(
    db_session, conversation_manager: "ConversationManager"
) -> None:
    """Тест что soft_delete возвращает количество удаленных записей"""
    key = ConversationKey(chat_id=9002, user_id=9002)

    # Добавляем сообщения
    await conversation_manager.add_message(key, ChatMessage(role="user", content="Test 1"))
    await conversation_manager.add_message(key, ChatMessage(role="user", content="Test 2"))

    # Удаляем
    repo = MessageRepository(db_session)
    deleted_count = await repo.soft_delete_history(key)

    assert deleted_count == 2  # noqa: PLR2004


@pytest.mark.asyncio
async def test_repository_add_message_with_length(
    db_session, conversation_manager: "ConversationManager"
) -> None:
    """Тест что при добавлении сохраняется длина контента"""
    key = ConversationKey(chat_id=9003, user_id=9003)
    message_content = "Test message with specific length"

    # Добавляем сообщение
    await conversation_manager.add_message(key, ChatMessage(role="user", content=message_content))

    # Получаем историю
    repo = MessageRepository(db_session)
    history = await repo.get_history(key, limit=10)

    assert len(history) == 1
    assert len(message_content) == len(history[0].content)
