from unittest.mock import AsyncMock

import pytest

from src.api.chat_handler import WebChatHandler, user_id_to_int
from src.api.models import ChatHistoryResponse
from src.models import ChatMessage


@pytest.mark.asyncio
async def test_user_id_to_int() -> None:
    """Test conversion of string user_id to integer."""
    user_id_1 = "web-user-1"
    user_id_2 = "web-user-2"

    int_id_1 = user_id_to_int(user_id_1)
    int_id_2 = user_id_to_int(user_id_2)

    # Should return consistent integers
    assert isinstance(int_id_1, int)
    assert isinstance(int_id_2, int)
    # Same input should produce same output
    assert user_id_to_int(user_id_1) == int_id_1
    # Different inputs should (likely) produce different outputs
    assert int_id_1 != int_id_2


@pytest.mark.asyncio
async def test_send_message_success() -> None:
    """Test successful message sending and receiving response."""
    # Mock dependencies
    mock_llm_client = AsyncMock()
    mock_conversation_manager = AsyncMock()

    # Setup mock responses
    mock_llm_client.get_response.return_value = "Hello, user!"
    mock_conversation_manager.add_message.return_value = None
    mock_conversation_manager.get_history.return_value = [
        ChatMessage(role="system", content="You are helpful"),
        ChatMessage(role="user", content="Hi"),
    ]

    handler = WebChatHandler(
        llm_client=mock_llm_client,
        conversation_manager=mock_conversation_manager,
        system_prompt="You are helpful",
    )

    # Test
    response, message_id = await handler.send_message(user_id="web-user-1", message="Hi")

    # Assertions
    assert response == "Hello, user!"
    assert isinstance(message_id, int)
    mock_conversation_manager.add_message.assert_called()
    mock_conversation_manager.get_history.assert_called()
    mock_llm_client.get_response.assert_called_once()


@pytest.mark.asyncio
async def test_send_message_error_handling() -> None:
    """Test error handling in send_message."""
    mock_llm_client = AsyncMock()
    mock_conversation_manager = AsyncMock()

    # Setup mock to raise error
    mock_llm_client.get_response.side_effect = Exception("LLM API error")
    mock_conversation_manager.add_message.return_value = None
    mock_conversation_manager.get_history.return_value = []

    handler = WebChatHandler(
        llm_client=mock_llm_client,
        conversation_manager=mock_conversation_manager,
        system_prompt="You are helpful",
    )

    # Test - should raise exception
    with pytest.raises(Exception, match="LLM API error"):
        await handler.send_message(user_id="web-user-1", message="Hi")


@pytest.mark.asyncio
async def test_get_history_success() -> None:
    """Test successful history retrieval."""
    mock_llm_client = AsyncMock()
    mock_conversation_manager = AsyncMock()

    # Setup mock responses
    mock_conversation_manager.get_history.return_value = [
        ChatMessage(role="system", content="You are helpful"),
        ChatMessage(role="user", content="Hello"),
        ChatMessage(role="assistant", content="Hi there"),
    ]

    handler = WebChatHandler(
        llm_client=mock_llm_client,
        conversation_manager=mock_conversation_manager,
        system_prompt="You are helpful",
    )

    # Test
    history = await handler.get_history(user_id="web-user-1")

    # Assertions
    assert isinstance(history, ChatHistoryResponse)
    # System message should be filtered out
    assert len(history.messages) == 2
    assert history.messages[0].role == "user"
    assert history.messages[1].role == "assistant"
    mock_conversation_manager.get_history.assert_called_once()


@pytest.mark.asyncio
async def test_get_history_empty() -> None:
    """Test history retrieval with empty history."""
    mock_llm_client = AsyncMock()
    mock_conversation_manager = AsyncMock()

    # Setup mock to return only system message
    mock_conversation_manager.get_history.return_value = [
        ChatMessage(role="system", content="You are helpful"),
    ]

    handler = WebChatHandler(
        llm_client=mock_llm_client,
        conversation_manager=mock_conversation_manager,
        system_prompt="You are helpful",
    )

    # Test
    history = await handler.get_history(user_id="web-user-1")

    # Assertions
    assert isinstance(history, ChatHistoryResponse)
    assert len(history.messages) == 0


@pytest.mark.asyncio
async def test_clear_history_success() -> None:
    """Test successful history clearing."""
    mock_llm_client = AsyncMock()
    mock_conversation_manager = AsyncMock()

    # Setup mock
    mock_conversation_manager.clear_history.return_value = None

    handler = WebChatHandler(
        llm_client=mock_llm_client,
        conversation_manager=mock_conversation_manager,
        system_prompt="You are helpful",
    )

    # Test
    deleted_count = await handler.clear_history(user_id="web-user-1")

    # Assertions
    assert isinstance(deleted_count, int)
    mock_conversation_manager.clear_history.assert_called_once()


@pytest.mark.asyncio
async def test_clear_history_error() -> None:
    """Test error handling in clear_history."""
    mock_llm_client = AsyncMock()
    mock_conversation_manager = AsyncMock()

    # Setup mock to raise error
    mock_conversation_manager.clear_history.side_effect = Exception("DB error")

    handler = WebChatHandler(
        llm_client=mock_llm_client,
        conversation_manager=mock_conversation_manager,
        system_prompt="You are helpful",
    )

    # Test - should raise exception
    with pytest.raises(Exception, match="DB error"):
        await handler.clear_history(user_id="web-user-1")
