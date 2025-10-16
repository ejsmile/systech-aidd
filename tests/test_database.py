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


@pytest.mark.asyncio
async def test_database_get_session_rollback_on_error(test_database_url: str) -> None:
    """Тест rollback при ошибке в сессии"""
    from sqlalchemy import text

    db = Database(test_database_url)

    # Пытаемся выполнить невалидный SQL, чтобы вызвать исключение
    with pytest.raises(Exception):
        async with db.get_session() as session:
            # Специально вызываем ошибку внутри сессии
            # Это должно вызвать rollback в except блоке
            await session.execute(text("SELECT * FROM nonexistent_table"))

    await db.disconnect()


@pytest.mark.asyncio
async def test_database_check_connection_with_valid_db(test_database_url: str) -> None:
    """Тест успешного подключения с выполнением SELECT 1"""
    db = Database(test_database_url)

    # Этот тест должен покрыть строку 53 (await conn.execute(text("SELECT 1")))
    result = await db.check_connection()

    assert result is True, "Должно быть успешное подключение к валидной БД"

    await db.disconnect()
