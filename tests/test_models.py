"""Тесты для моделей данных"""

from unittest.mock import Mock

from src.models import ChatMessage, ConversationKey, Role, UserData, extract_user_data


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


def test_user_data_frozen() -> None:
    """UserData должен быть immutable"""
    user_data = UserData(
        user_id=123456,  # noqa: PLR2004
        username="testuser",
        first_name="Test",
        last_name="User",
    )

    assert user_data.user_id == 123456  # noqa: PLR2004
    assert user_data.username == "testuser"
    assert user_data.first_name == "Test"
    assert user_data.last_name == "User"

    # Должна быть ошибка при попытке изменить
    try:
        user_data.username = "newname"  # type: ignore[misc]
        raise AssertionError("UserData должен быть frozen")
    except AttributeError:
        pass


def test_user_data_to_dict() -> None:
    """UserData.to_dict() должен возвращать dict для UserRepository"""
    user_data = UserData(
        user_id=123456,  # noqa: PLR2004
        username="testuser",
        first_name="Test",
        last_name="User",
    )

    result = user_data.to_dict()

    assert result == {
        "user_id": 123456,  # noqa: PLR2004
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
    }


def test_user_data_with_nullable_fields() -> None:
    """UserData должен поддерживать nullable поля"""
    user_data = UserData(
        user_id=999888,  # noqa: PLR2004
        username=None,
        first_name="NoUsername",
        last_name=None,
    )

    assert user_data.user_id == 999888  # noqa: PLR2004
    assert user_data.username is None
    assert user_data.first_name == "NoUsername"
    assert user_data.last_name is None


def test_extract_user_data_full() -> None:
    """extract_user_data() должен извлекать все данные"""
    # Mock Telegram User с полными данными
    telegram_user = Mock()
    telegram_user.id = 123456  # noqa: PLR2004
    telegram_user.username = "testuser"
    telegram_user.first_name = "Test"
    telegram_user.last_name = "User"

    result = extract_user_data(telegram_user)

    assert result.user_id == 123456  # noqa: PLR2004
    assert result.username == "testuser"
    assert result.first_name == "Test"
    assert result.last_name == "User"


def test_extract_user_data_without_username() -> None:
    """extract_user_data() должен обрабатывать отсутствие username"""
    # Mock Telegram User без username
    telegram_user = Mock()
    telegram_user.id = 999888  # noqa: PLR2004
    telegram_user.username = None
    telegram_user.first_name = "NoUsername"
    telegram_user.last_name = None

    result = extract_user_data(telegram_user)

    assert result.user_id == 999888  # noqa: PLR2004
    assert result.username is None
    assert result.first_name == "NoUsername"
    assert result.last_name is None


def test_extract_user_data_without_last_name() -> None:
    """extract_user_data() должен обрабатывать отсутствие last_name"""
    # Mock Telegram User без last_name
    telegram_user = Mock()
    telegram_user.id = 777666  # noqa: PLR2004
    telegram_user.username = "singlename"
    telegram_user.first_name = "Single"
    telegram_user.last_name = None

    result = extract_user_data(telegram_user)

    assert result.user_id == 777666  # noqa: PLR2004
    assert result.username == "singlename"
    assert result.first_name == "Single"
    assert result.last_name is None
