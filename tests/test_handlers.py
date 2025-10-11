"""Тесты для обработчиков команд и сообщений"""

from unittest.mock import AsyncMock, Mock

import pytest

from src.conversation import ConversationManager
from src.handlers import (
    cmd_clear,
    cmd_help,
    cmd_role,
    cmd_start,
    handle_message,
    handle_unsupported,
)
from src.llm_client import LLMClient
from src.models import ChatMessage


@pytest.fixture
def mock_message() -> Mock:
    """Mock объект aiogram Message"""
    message = Mock()
    message.from_user = Mock()
    message.from_user.id = 12345
    message.chat = Mock()
    message.chat.id = 67890
    message.text = "Test message"
    message.answer = AsyncMock()
    return message


@pytest.fixture
def mock_llm_client() -> Mock:
    """Mock LLMClient"""
    client = Mock(spec=LLMClient)
    client.get_response = AsyncMock(return_value="LLM response")
    return client


@pytest.mark.asyncio
async def test_cmd_start(mock_message: Mock) -> None:
    """Тест команды /start"""
    await cmd_start(mock_message)

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args[0][0]
    assert "Привет! Я LLM-ассистент" in call_args
    assert "/help" in call_args


@pytest.mark.asyncio
async def test_cmd_start_no_user(mock_message: Mock) -> None:
    """Тест команды /start без from_user"""
    mock_message.from_user = None
    await cmd_start(mock_message)

    # Не должно быть вызова answer
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_cmd_help(mock_message: Mock) -> None:
    """Тест команды /help"""
    await cmd_help(mock_message)

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args[0][0]
    assert "/start" in call_args
    assert "/help" in call_args
    assert "/clear" in call_args
    assert "/role" in call_args


@pytest.mark.asyncio
async def test_cmd_help_no_user(mock_message: Mock) -> None:
    """Тест команды /help без from_user"""
    mock_message.from_user = None
    await cmd_help(mock_message)

    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_cmd_clear(mock_message: Mock, conversation_manager: ConversationManager) -> None:
    """Тест команды /clear"""
    # Добавляем сообщения в историю
    key = conversation_manager.get_conversation_key(
        chat_id=mock_message.chat.id,
        user_id=mock_message.from_user.id,
    )
    conversation_manager.add_message(key, ChatMessage(role="user", content="Test"))

    # Проверяем, что история не пустая
    assert len(conversation_manager.conversations[key]) > 0

    # Вызываем команду clear
    await cmd_clear(mock_message, conversation_manager)

    # Проверяем, что история очищена
    assert key not in conversation_manager.conversations
    mock_message.answer.assert_called_once_with("История диалога очищена")


@pytest.mark.asyncio
async def test_cmd_clear_no_user(
    mock_message: Mock, conversation_manager: ConversationManager
) -> None:
    """Тест команды /clear без from_user"""
    mock_message.from_user = None
    await cmd_clear(mock_message, conversation_manager)

    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_success(
    mock_message: Mock,
    mock_llm_client: Mock,
    conversation_manager: ConversationManager,
) -> None:
    """Тест успешной обработки текстового сообщения"""
    system_prompt = "You are a helpful assistant"
    mock_message.text = "Hello, bot!"

    await handle_message(mock_message, mock_llm_client, conversation_manager, system_prompt)

    # Проверяем, что LLM был вызван
    mock_llm_client.get_response.assert_called_once()

    # Проверяем, что сообщения добавлены в историю
    key = conversation_manager.get_conversation_key(
        chat_id=mock_message.chat.id,
        user_id=mock_message.from_user.id,
    )
    history = conversation_manager.get_history(key, system_prompt)

    # В истории должно быть: system, user, assistant
    assert len(history) == 3  # noqa: PLR2004
    assert history[0].role == "system"
    assert history[1].role == "user"
    assert history[1].content == "Hello, bot!"
    assert history[2].role == "assistant"
    assert history[2].content == "LLM response"

    # Проверяем, что ответ отправлен пользователю
    mock_message.answer.assert_called_once_with("LLM response")


@pytest.mark.asyncio
async def test_handle_message_no_user(
    mock_message: Mock,
    mock_llm_client: Mock,
    conversation_manager: ConversationManager,
) -> None:
    """Тест обработки сообщения без from_user"""
    mock_message.from_user = None
    system_prompt = "System prompt"

    await handle_message(mock_message, mock_llm_client, conversation_manager, system_prompt)

    mock_llm_client.get_response.assert_not_called()
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_no_text(
    mock_message: Mock,
    mock_llm_client: Mock,
    conversation_manager: ConversationManager,
) -> None:
    """Тест обработки сообщения без текста"""
    mock_message.text = None
    system_prompt = "System prompt"

    await handle_message(mock_message, mock_llm_client, conversation_manager, system_prompt)

    mock_llm_client.get_response.assert_not_called()
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_llm_error(
    mock_message: Mock,
    mock_llm_client: Mock,
    conversation_manager: ConversationManager,
) -> None:
    """Тест обработки ошибки LLM API"""
    system_prompt = "System prompt"
    mock_message.text = "Test message"

    # Симулируем ошибку LLM
    mock_llm_client.get_response.side_effect = Exception("API Error")

    await handle_message(mock_message, mock_llm_client, conversation_manager, system_prompt)

    # Проверяем, что пользователю отправлено сообщение об ошибке
    mock_message.answer.assert_called_once()
    error_message = mock_message.answer.call_args[0][0]
    assert "ошибка" in error_message.lower()


@pytest.mark.asyncio
async def test_handle_message_conversation_history(
    mock_message: Mock,
    mock_llm_client: Mock,
) -> None:
    """Тест сохранения истории диалога"""
    # Используем ConversationManager с достаточным лимитом истории
    manager = ConversationManager(max_history_messages=10)
    system_prompt = "System prompt"

    # Первое сообщение
    mock_message.text = "First message"
    await handle_message(mock_message, mock_llm_client, manager, system_prompt)

    # Второе сообщение
    mock_message.text = "Second message"
    mock_llm_client.get_response.return_value = "Second response"
    await handle_message(mock_message, mock_llm_client, manager, system_prompt)

    # Проверяем историю
    key = manager.get_conversation_key(
        chat_id=mock_message.chat.id,
        user_id=mock_message.from_user.id,
    )
    history = manager.get_history(key, system_prompt)

    # System + 2 пары (user + assistant)
    assert len(history) == 5  # noqa: PLR2004
    assert history[1].content == "First message"
    assert history[2].content == "LLM response"
    assert history[3].content == "Second message"
    assert history[4].content == "Second response"


@pytest.mark.asyncio
async def test_handle_unsupported(mock_message: Mock) -> None:
    """Тест обработки неподдерживаемых типов сообщений"""
    await handle_unsupported(mock_message)

    # Не должно быть ответа пользователю (тихо игнорируем)
    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_handle_unsupported_no_user(mock_message: Mock) -> None:
    """Тест обработки неподдерживаемых сообщений без from_user"""
    mock_message.from_user = None
    await handle_unsupported(mock_message)

    mock_message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_cmd_role(mock_message: Mock) -> None:
    """Тест команды /role"""
    system_prompt = "Ты тестовый бот."
    await cmd_role(mock_message, system_prompt)

    mock_message.answer.assert_called_once()
    call_args = mock_message.answer.call_args[0][0]
    assert "Ты тестовый бот." in call_args


@pytest.mark.asyncio
async def test_cmd_role_no_user(mock_message: Mock) -> None:
    """Тест команды /role без from_user"""
    mock_message.from_user = None
    system_prompt = "Test prompt"
    await cmd_role(mock_message, system_prompt)

    mock_message.answer.assert_not_called()
