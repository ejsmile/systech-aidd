"""Тесты для моделей данных"""

from src.models import ChatMessage, ConversationKey, Role


def test_conversation_key_frozen() -> None:
    """ConversationKey должен быть immutable"""
    key = ConversationKey(chat_id=1, user_id=1)
    assert key.chat_id == 1
    assert key.user_id == 1

    # Должна быть ошибка при попытке изменить
    try:
        key.chat_id = 2  # type: ignore[misc]
        raise AssertionError("ConversationKey должен быть frozen")
    except AttributeError:
        pass


def test_conversation_key_hashable() -> None:
    """ConversationKey должен быть hashable для использования как ключ dict"""
    key1 = ConversationKey(chat_id=1, user_id=1)
    key2 = ConversationKey(chat_id=1, user_id=1)
    key3 = ConversationKey(chat_id=2, user_id=1)

    assert key1 == key2
    assert key1 != key3
    assert hash(key1) == hash(key2)


def test_chat_message_to_dict() -> None:
    """ChatMessage.to_dict() должен возвращать формат OpenAI API"""
    msg = ChatMessage(role="user", content="test")
    result = msg.to_dict()

    assert result == {"role": "user", "content": "test"}


def test_role_enum() -> None:
    """Role enum должен содержать правильные значения"""
    assert Role.SYSTEM == "system"
    assert Role.USER == "user"
    assert Role.ASSISTANT == "assistant"
