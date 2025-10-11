"""Тесты для ConversationManager"""

import pytest

from src.conversation import ConversationManager
from src.models import ChatMessage, ConversationKey


@pytest.fixture
def manager() -> ConversationManager:
    return ConversationManager(max_history_messages=3)


def test_add_message(manager: ConversationManager) -> None:
    """Добавление сообщения в историю"""
    key = ConversationKey(chat_id=1, user_id=1)
    msg = ChatMessage(role="user", content="test")

    manager.add_message(key, msg)

    assert key in manager.conversations
    assert len(manager.conversations[key]) == 1
    assert manager.conversations[key][0] == msg


def test_get_history_with_system_prompt(manager: ConversationManager) -> None:
    """История должна включать system prompt"""
    key = ConversationKey(chat_id=1, user_id=1)
    system_prompt = "You are helpful assistant"

    history = manager.get_history(key, system_prompt)

    assert len(history) == 1
    assert history[0].role == "system"
    assert history[0].content == system_prompt


def test_history_limit(manager: ConversationManager) -> None:
    """История должна ограничиваться max_history_messages"""
    key = ConversationKey(chat_id=1, user_id=1)
    system_prompt = "test"

    # Добавляем 5 сообщений (limit = 3)
    for i in range(5):
        manager.add_message(key, ChatMessage(role="user", content=f"msg{i}"))

    history = manager.get_history(key, system_prompt)

    # system + 3 последних сообщения
    expected_length = 1 + 3  # system prompt + max_history_messages
    assert len(history) == expected_length
    assert history[0].role == "system"
    assert history[-1].content == "msg4"  # последнее
    assert history[1].content == "msg2"  # 3-е с конца


def test_clear_history(manager: ConversationManager) -> None:
    """Очистка истории диалога"""
    key = ConversationKey(chat_id=1, user_id=1)
    manager.add_message(key, ChatMessage(role="user", content="test"))

    assert key in manager.conversations

    manager.clear_history(key)

    assert key not in manager.conversations


def test_multiple_conversations(manager: ConversationManager) -> None:
    """Разные пользователи имеют разные истории"""
    key1 = ConversationKey(chat_id=1, user_id=1)
    key2 = ConversationKey(chat_id=1, user_id=2)

    manager.add_message(key1, ChatMessage(role="user", content="user1"))
    manager.add_message(key2, ChatMessage(role="user", content="user2"))

    assert len(manager.conversations[key1]) == 1
    assert len(manager.conversations[key2]) == 1
    assert manager.conversations[key1][0].content == "user1"
    assert manager.conversations[key2][0].content == "user2"
