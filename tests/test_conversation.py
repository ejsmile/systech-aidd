"""Тесты для ConversationManager"""

import pytest

from src.conversation import ConversationManager
from src.models import ChatMessage, ConversationKey


@pytest.mark.asyncio
async def test_add_message(conversation_manager: ConversationManager) -> None:
    """Добавление сообщения в историю"""
    key = ConversationKey(chat_id=1, user_id=1)
    msg = ChatMessage(role="user", content="test")

    await conversation_manager.add_message(key, msg)

    # Проверяем через get_history
    history = await conversation_manager.get_history(key, "system")
    user_messages = [m for m in history if m.role == "user"]
    assert len(user_messages) == 1
    assert user_messages[0].content == "test"


@pytest.mark.asyncio
async def test_get_history_with_system_prompt(
    conversation_manager: ConversationManager,
) -> None:
    """История должна включать system prompt"""
    key = ConversationKey(chat_id=2, user_id=2)
    system_prompt = "You are helpful assistant"

    history = await conversation_manager.get_history(key, system_prompt)

    assert len(history) == 1
    assert history[0].role == "system"
    assert history[0].content == system_prompt


@pytest.mark.asyncio
async def test_history_limit(conversation_manager: ConversationManager) -> None:
    """История должна ограничиваться max_history_messages"""
    key = ConversationKey(chat_id=3, user_id=3)
    system_prompt = "test"

    # Добавляем 5 сообщений (limit = 3)
    for i in range(5):
        await conversation_manager.add_message(key, ChatMessage(role="user", content=f"msg{i}"))

    history = await conversation_manager.get_history(key, system_prompt)

    # system + 3 последних сообщения
    expected_length = 1 + 3  # system prompt + max_history_messages
    assert len(history) == expected_length
    assert history[0].role == "system"
    assert history[-1].content == "msg4"  # последнее
    assert history[1].content == "msg2"  # 3-е с конца


@pytest.mark.asyncio
async def test_clear_history(conversation_manager: ConversationManager) -> None:
    """Очистка истории диалога (soft delete)"""
    key = ConversationKey(chat_id=4, user_id=4)
    await conversation_manager.add_message(key, ChatMessage(role="user", content="test"))

    # Проверяем, что сообщение есть
    history_before = await conversation_manager.get_history(key, "system")
    expected_messages = 2  # system + user message
    assert len(history_before) == expected_messages

    # Очищаем историю
    await conversation_manager.clear_history(key)

    # Проверяем, что история пуста (soft delete)
    history_after = await conversation_manager.get_history(key, "system")
    # После clear должен остаться только новый system prompt
    assert len(history_after) == 1
    assert history_after[0].role == "system"


@pytest.mark.asyncio
async def test_multiple_conversations(conversation_manager: ConversationManager) -> None:
    """Разные пользователи имеют разные истории"""
    key1 = ConversationKey(chat_id=5, user_id=5)
    key2 = ConversationKey(chat_id=5, user_id=6)

    await conversation_manager.add_message(key1, ChatMessage(role="user", content="user1"))
    await conversation_manager.add_message(key2, ChatMessage(role="user", content="user2"))

    history1 = await conversation_manager.get_history(key1, "system")
    history2 = await conversation_manager.get_history(key2, "system")

    user1_messages = [m for m in history1 if m.role == "user"]
    user2_messages = [m for m in history2 if m.role == "user"]

    assert len(user1_messages) == 1
    assert len(user2_messages) == 1
    assert user1_messages[0].content == "user1"
    assert user2_messages[0].content == "user2"
