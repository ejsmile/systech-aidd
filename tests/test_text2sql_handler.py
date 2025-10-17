from unittest.mock import AsyncMock

import pytest

from src.api.text2sql_handler import Text2SQLHandler


@pytest.mark.asyncio
async def test_validate_sql_select_query() -> None:
    """Test validation of simple SELECT query."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "SELECT * FROM users"
    assert handler.validate_sql(sql) is True


@pytest.mark.asyncio
async def test_validate_sql_select_with_where() -> None:
    """Test validation of SELECT query with WHERE clause."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "SELECT id, username FROM users WHERE id > 5"
    assert handler.validate_sql(sql) is True


@pytest.mark.asyncio
async def test_validate_sql_select_messages_table() -> None:
    """Test validation of SELECT query from messages table."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "SELECT * FROM messages WHERE deleted_at IS NULL"
    assert handler.validate_sql(sql) is True


@pytest.mark.asyncio
async def test_validate_sql_not_select() -> None:
    """Test validation fails for non-SELECT queries."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "INSERT INTO users (username) VALUES ('hack')"
    assert handler.validate_sql(sql) is False


@pytest.mark.asyncio
async def test_validate_sql_delete_query() -> None:
    """Test validation fails for DELETE queries."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "DELETE FROM users WHERE id = 1"
    assert handler.validate_sql(sql) is False


@pytest.mark.asyncio
async def test_validate_sql_update_query() -> None:
    """Test validation fails for UPDATE queries."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "UPDATE users SET username = 'hack' WHERE id = 1"
    assert handler.validate_sql(sql) is False


@pytest.mark.asyncio
async def test_validate_sql_drop_query() -> None:
    """Test validation fails for DROP queries."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "DROP TABLE users"
    assert handler.validate_sql(sql) is False


@pytest.mark.asyncio
async def test_validate_sql_create_query() -> None:
    """Test validation fails for CREATE queries."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "CREATE TABLE fake_table (id INT)"
    assert handler.validate_sql(sql) is False


@pytest.mark.asyncio
async def test_validate_sql_alter_query() -> None:
    """Test validation fails for ALTER queries."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "ALTER TABLE users ADD COLUMN fake_col VARCHAR"
    assert handler.validate_sql(sql) is False


@pytest.mark.asyncio
async def test_validate_sql_forbidden_table() -> None:
    """Test validation fails for non-whitelisted tables."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "SELECT * FROM forbidden_table"
    assert handler.validate_sql(sql) is False


@pytest.mark.asyncio
async def test_validate_sql_case_insensitive() -> None:
    """Test validation is case-insensitive."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "select * from users"
    assert handler.validate_sql(sql) is True

    sql = "SELECT * FROM USERS"
    assert handler.validate_sql(sql) is True


@pytest.mark.asyncio
async def test_validate_sql_with_comments() -> None:
    """Test validation handles SQL comments."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    sql = "-- This is a comment\nSELECT * FROM users"
    assert handler.validate_sql(sql) is True


@pytest.mark.asyncio
async def test_execute_sql_invalid_query() -> None:
    """Test execute_sql fails for invalid query."""
    handler = Text2SQLHandler(
        llm_client=AsyncMock(),
        session_factory=AsyncMock(),
        text2sql_prompt="Test prompt",
    )

    with pytest.raises(ValueError):
        await handler.execute_sql("DELETE FROM users")
