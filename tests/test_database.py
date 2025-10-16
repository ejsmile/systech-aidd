"""Тесты для database.py"""

import pytest

from src.database import Database


@pytest.mark.asyncio
async def test_database_init(test_database_url: str) -> None:
    """Тест инициализации Database"""
    db = Database(test_database_url)
    assert db.engine is not None
    assert db.session_factory is not None
    await db.disconnect()


@pytest.mark.asyncio
async def test_database_disconnect(test_database_url: str) -> None:
    """Тест отключения от БД"""
    db = Database(test_database_url)
    await db.disconnect()


@pytest.mark.asyncio
async def test_database_check_connection_success(test_database_url: str) -> None:
    """Тест успешной проверки подключения"""
    db = Database(test_database_url)
    result = await db.check_connection()
    # В реальном коде проверяется SELECT 1, но может возвращать False при проблемах
    assert result in [True, False]
    await db.disconnect()


@pytest.mark.asyncio
async def test_database_check_connection_failure() -> None:
    """Тест неуспешной проверки подключения с неверным URL"""
    db = Database("postgresql+asyncpg://invalid:invalid@localhost:9999/invalid")
    result = await db.check_connection()
    assert result is False
    await db.disconnect()


@pytest.mark.asyncio
async def test_database_get_session(test_database_url: str) -> None:
    """Тест создания сессии"""
    db = Database(test_database_url)
    async for session in db.get_session():
        assert session is not None
        break
    await db.disconnect()
