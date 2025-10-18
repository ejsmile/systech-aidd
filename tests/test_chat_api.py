from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.app import app

# Unused sync client fixture removed - all tests now use async_client


@pytest.fixture
async def async_client(
    test_database_url: str, apply_migrations: None
) -> AsyncGenerator[AsyncClient, None]:
    """Fixture to provide async client for FastAPI app (for tests with DB)."""
    from src.api.chat_handler import WebChatHandler  # noqa: PLC0415
    from src.api.text2sql_handler import Text2SQLHandler  # noqa: PLC0415
    from src.config import Config  # noqa: PLC0415
    from src.conversation import ConversationManager  # noqa: PLC0415
    from src.database import Database  # noqa: PLC0415
    from src.llm_client import LLMClient  # noqa: PLC0415

    # Create fresh database instance for testing with testcontainer
    database = Database(test_database_url)

    # Initialize handlers with test database
    try:
        with open("prompts/text2sql.txt", encoding="utf-8") as f:
            text2sql_prompt = f.read().strip()
    except FileNotFoundError:
        text2sql_prompt = "Generate SQL queries for the given questions."

    config = Config(  # type: ignore[call-arg]
        telegram_token="test_token",
        openrouter_api_key="test_api_key",
    )
    llm_client = LLMClient(config)
    conversation_manager = ConversationManager(
        session_factory=database.get_session,
        max_history_messages=20,
    )

    chat_handler = WebChatHandler(
        llm_client=llm_client,
        conversation_manager=conversation_manager,
        system_prompt="Test system prompt",
    )

    text2sql_handler = Text2SQLHandler(
        llm_client=llm_client,
        session_factory=database.get_session,
        text2sql_prompt=text2sql_prompt,
    )

    # Override app dependencies
    import src.api.app as app_module  # noqa: PLC0415

    original_chat_handler = app_module.chat_handler
    original_text2sql_handler = app_module.text2sql_handler
    app_module.chat_handler = chat_handler
    app_module.text2sql_handler = text2sql_handler

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client
    finally:
        # Restore original handlers
        app_module.chat_handler = original_chat_handler
        app_module.text2sql_handler = original_text2sql_handler
        await database.disconnect()


@pytest.mark.asyncio
async def test_chat_message_success(async_client: AsyncClient) -> None:
    """Test successful chat message endpoint."""
    # Mock LLM response
    with patch("src.llm_client.LLMClient.get_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Test response from bot"

        payload = {"user_id": "test-user-1", "message": "Hello!"}

        response = await async_client.post("/api/v1/chat/message", json=payload)

        # Should return 200 with valid response
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "message_id" in data
        assert isinstance(data["response"], str)
        assert isinstance(data["message_id"], int)


@pytest.mark.asyncio
async def test_chat_message_empty_message(async_client: AsyncClient) -> None:
    """Test chat message with empty message (validation error)."""
    payload = {"user_id": "test-user-1", "message": ""}

    response = await async_client.post("/api/v1/chat/message", json=payload)

    # Should return 422 (validation error)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_message_missing_user_id(async_client: AsyncClient) -> None:
    """Test chat message with missing user_id (validation error)."""
    payload = {"message": "Hello!"}

    response = await async_client.post("/api/v1/chat/message", json=payload)

    # Should return 422 (validation error)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_message_missing_message(async_client: AsyncClient) -> None:
    """Test chat message with missing message (validation error)."""
    payload = {"user_id": "test-user-1"}

    response = await async_client.post("/api/v1/chat/message", json=payload)

    # Should return 422 (validation error)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_message_too_long(async_client: AsyncClient) -> None:
    """Test chat message that exceeds max length."""
    long_message = "x" * 5000  # Exceeds 4000 char limit

    payload = {"user_id": "test-user-1", "message": long_message}

    response = await async_client.post("/api/v1/chat/message", json=payload)

    # Should return 422 (validation error)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_chat_history_success(async_client: AsyncClient) -> None:
    """Test successful chat history retrieval."""
    # Mock LLM response
    with patch("src.llm_client.LLMClient.get_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Test response from bot"

        # First send a message
        payload = {"user_id": "test-user-1", "message": "Hello!"}
        await async_client.post("/api/v1/chat/message", json=payload)

        # Then get history
        response = await async_client.get("/api/v1/chat/history/test-user-1")

        # Should return 200 with valid response
        assert response.status_code == 200
        data = response.json()
        assert "messages" in data
        assert isinstance(data["messages"], list)


@pytest.mark.asyncio
async def test_get_chat_history_empty_user(async_client: AsyncClient) -> None:
    """Test history retrieval for user with no messages."""
    response = await async_client.get("/api/v1/chat/history/nonexistent-user")

    # Should return 200 with empty history
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert isinstance(data["messages"], list)


@pytest.mark.asyncio
async def test_clear_chat_history_success(async_client: AsyncClient) -> None:
    """Test successful chat history clearing."""
    # Mock LLM response
    with patch("src.llm_client.LLMClient.get_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Test response from bot"

        # First send a message
        payload = {"user_id": "test-user-2", "message": "Hello!"}
        await async_client.post("/api/v1/chat/message", json=payload)

        # Then clear history
        response = await async_client.delete("/api/v1/chat/history/test-user-2")

        # Should return 200 with valid response
        assert response.status_code == 200
        data = response.json()
        assert "success" in data
        assert isinstance(data["success"], bool)
        assert "deleted_count" in data
        assert isinstance(data["deleted_count"], int)


@pytest.mark.asyncio
async def test_clear_chat_history_nonexistent_user(async_client: AsyncClient) -> None:
    """Test clearing history for user with no messages."""
    response = await async_client.delete("/api/v1/chat/history/nonexistent-user-2")

    # Should return 200 (no error, just empty result)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_chat_endpoints_cors_headers(async_client: AsyncClient) -> None:
    """Test that CORS headers are present for OPTIONS request."""
    # Test OPTIONS preflight request
    response = await async_client.options(
        "/api/v1/statistics",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    # Check CORS headers in OPTIONS response
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers


@pytest.mark.asyncio
async def test_chat_message_response_model_validation(async_client: AsyncClient) -> None:
    """Test that response matches ChatMessageResponse model."""
    # Mock LLM response
    with patch("src.llm_client.LLMClient.get_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "Test response from bot"

        payload = {"user_id": "test-user-3", "message": "Test"}

        response = await async_client.post("/api/v1/chat/message", json=payload)

        assert response.status_code == 200
        data = response.json()

        # Validate required fields
        assert set(data.keys()) == {"response", "message_id"}


@pytest.mark.asyncio
async def test_chat_history_response_model_validation(async_client: AsyncClient) -> None:
    """Test that response matches ChatHistoryResponse model."""
    response = await async_client.get("/api/v1/chat/history/test-user-4")

    assert response.status_code == 200
    data = response.json()

    # Validate required fields
    assert "messages" in data
    assert isinstance(data["messages"], list)

    # Each message should have required fields
    if data["messages"]:
        message = data["messages"][0]
        assert "role" in message
        assert "content" in message
        assert "created_at" in message


@pytest.mark.asyncio
async def test_clear_history_response_model_validation(async_client: AsyncClient) -> None:
    """Test that response matches ClearHistoryResponse model."""
    response = await async_client.delete("/api/v1/chat/history/test-user-5")

    assert response.status_code == 200
    data = response.json()

    # Validate required fields
    assert set(data.keys()) == {"success", "deleted_count"}
    assert isinstance(data["success"], bool)
    assert isinstance(data["deleted_count"], int)


@pytest.mark.asyncio
async def test_admin_query_success(async_client: AsyncClient) -> None:
    """Test successful admin query endpoint."""
    # Mock LLM response to return valid SQL
    with patch("src.llm_client.LLMClient.get_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "```sql\nSELECT COUNT(*) as count FROM users\n```"

        payload = {"query": "How many users are there?"}

        response = await async_client.post("/api/v1/admin/query", json=payload)

        # Should return 200
        assert response.status_code == 200
        data = response.json()
        assert "sql" in data
        assert "result" in data
        assert "interpretation" in data


@pytest.mark.asyncio
async def test_admin_query_empty_query(async_client: AsyncClient) -> None:
    """Test admin query with empty query (validation error)."""
    payload = {"query": ""}

    response = await async_client.post("/api/v1/admin/query", json=payload)

    # Should return 400 (ValueError caught and converted to HTTPException)
    assert response.status_code == 400
    # Check that error message is present
    data = response.json()
    assert "detail" in data
    assert "empty" in data["detail"].lower()


@pytest.mark.asyncio
async def test_admin_query_missing_query(async_client: AsyncClient) -> None:
    """Test admin query with missing query field (validation error)."""
    payload = {}

    response = await async_client.post("/api/v1/admin/query", json=payload)

    # Should return 422 (validation error)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_admin_query_response_structure(async_client: AsyncClient) -> None:
    """Test that admin query response has correct structure if successful."""
    # Mock LLM response to return valid SQL
    with patch("src.llm_client.LLMClient.get_response", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = "```sql\nSELECT COUNT(*) as total FROM users\n```"

        payload = {"query": "SELECT COUNT(*) as total FROM users"}

        response = await async_client.post("/api/v1/admin/query", json=payload)

        # Should return 200 with proper structure
        assert response.status_code == 200
        data = response.json()
        assert "sql" in data
        assert "result" in data
        assert "interpretation" in data
        assert isinstance(data["sql"], str)
        assert isinstance(data["result"], list)
        assert isinstance(data["interpretation"], str)
