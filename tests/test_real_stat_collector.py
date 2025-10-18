"""Тесты для RealStatCollector."""

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import StatisticsResponse
from src.api.real_stat_collector import RealStatCollector
from src.db_models import Message, User


@pytest.mark.asyncio
async def test_real_stat_collector_empty_database(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector с пустой БД."""

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)
    stats = await collector.get_statistics()

    assert isinstance(stats, StatisticsResponse)
    assert stats.total_users == 0
    assert stats.active_users == 0
    assert stats.total_messages == 0
    assert stats.avg_messages_per_user == 0.0
    assert stats.messages_by_date == []
    assert stats.top_users == []


@pytest.mark.asyncio
async def test_real_stat_collector_with_users(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector с пользователями без сообщений."""
    # Создаем пользователей
    user1 = User(user_id=1001, username="test_user1", first_name="Test")
    user2 = User(user_id=1002, username="test_user2", first_name="User2")
    clean_db_session.add_all([user1, user2])
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)
    stats = await collector.get_statistics()

    assert stats.total_users == 2
    assert stats.active_users == 0  # Нет сообщений
    assert stats.total_messages == 0
    assert stats.avg_messages_per_user == 0.0


@pytest.mark.asyncio
async def test_real_stat_collector_with_messages(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector с пользователями и сообщениями."""
    now = datetime.now()

    # Создаем пользователей
    user1 = User(user_id=2001, username="active_user", first_name="Active")
    user2 = User(user_id=2002, username=None, first_name="NoUsername")
    clean_db_session.add_all([user1, user2])
    await clean_db_session.commit()

    # Создаем сообщения
    messages = [
        Message(
            chat_id=2001,
            user_id=2001,
            role="user",
            content="Message 1",
            content_length=9,
            created_at=now - timedelta(days=1),
        ),
        Message(
            chat_id=2001,
            user_id=2001,
            role="assistant",
            content="Response 1",
            content_length=10,
            created_at=now - timedelta(days=1),
        ),
        Message(
            chat_id=2002,
            user_id=2002,
            role="user",
            content="Message 2",
            content_length=9,
            created_at=now - timedelta(days=5),
        ),
    ]
    clean_db_session.add_all(messages)
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)
    stats = await collector.get_statistics()

    assert stats.total_users == 2
    assert stats.active_users == 2  # Оба пользователя активны (за 30 дней)
    assert stats.total_messages == 3
    assert stats.avg_messages_per_user == 1.5  # 3 / 2
    assert len(stats.messages_by_date) > 0
    assert len(stats.top_users) == 2
    assert stats.top_users[0].user_id == 2001  # Первый пользователь более активен
    assert stats.top_users[0].message_count == 2
    assert stats.top_users[0].username == "active_user"
    assert stats.top_users[1].user_id == 2002
    assert stats.top_users[1].message_count == 1
    assert stats.top_users[1].username is None


@pytest.mark.asyncio
async def test_real_stat_collector_with_deleted_messages(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector игнорирует удаленные сообщения."""
    now = datetime.now()

    # Создаем пользователя
    user = User(user_id=3001, username="user", first_name="User")
    clean_db_session.add(user)
    await clean_db_session.commit()

    # Создаем сообщения (одно удаленное)
    messages = [
        Message(
            chat_id=3001,
            user_id=3001,
            role="user",
            content="Active message",
            content_length=14,
            created_at=now - timedelta(days=1),
        ),
        Message(
            chat_id=3001,
            user_id=3001,
            role="user",
            content="Deleted message",
            content_length=15,
            created_at=now - timedelta(days=2),
            deleted_at=now - timedelta(hours=1),
        ),
    ]
    clean_db_session.add_all(messages)
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)
    stats = await collector.get_statistics()

    assert stats.total_users == 1
    assert stats.active_users == 1
    assert stats.total_messages == 1  # Только не удаленное
    assert stats.top_users[0].message_count == 1


@pytest.mark.asyncio
async def test_real_stat_collector_date_filtering(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector с фильтрацией по датам."""
    now = datetime.now()

    # Создаем пользователя
    user = User(user_id=4001, username="user", first_name="User")
    clean_db_session.add(user)
    await clean_db_session.commit()

    # Создаем сообщения в разные даты
    messages = [
        Message(
            chat_id=4001,
            user_id=4001,
            role="user",
            content="Old message",
            content_length=11,
            created_at=now - timedelta(days=40),
        ),
        Message(
            chat_id=4001,
            user_id=4001,
            role="user",
            content="Recent message",
            content_length=14,
            created_at=now - timedelta(days=5),
        ),
    ]
    clean_db_session.add_all(messages)
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)

    # Получить статистику за последние 30 дней
    stats = await collector.get_statistics()
    assert stats.total_messages == 1  # Только недавнее сообщение

    # Получить статистику за весь период
    start_date = now - timedelta(days=50)
    stats_all = await collector.get_statistics(start_date=start_date)
    assert stats_all.total_messages == 2  # Оба сообщения


@pytest.mark.asyncio
async def test_real_stat_collector_messages_by_date(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector группировки по датам."""
    now = datetime.now()

    # Создаем пользователя
    user = User(user_id=5001, username="user", first_name="User")
    clean_db_session.add(user)
    await clean_db_session.commit()

    # Создаем несколько сообщений в один день и одно в другой день
    today = now.replace(hour=10, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    messages = [
        Message(
            chat_id=5001,
            user_id=5001,
            role="user",
            content="Message 1",
            content_length=9,
            created_at=today,
        ),
        Message(
            chat_id=5001,
            user_id=5001,
            role="user",
            content="Message 2",
            content_length=9,
            created_at=today.replace(hour=15),
        ),
        Message(
            chat_id=5001,
            user_id=5001,
            role="user",
            content="Message 3",
            content_length=9,
            created_at=yesterday,
        ),
    ]
    clean_db_session.add_all(messages)
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)
    stats = await collector.get_statistics()

    assert len(stats.messages_by_date) == 2
    # Сортировка по дате (старые первые)
    assert stats.messages_by_date[0].count == 1  # вчера
    assert stats.messages_by_date[1].count == 2  # сегодня


@pytest.mark.asyncio
async def test_real_stat_collector_top_users_limit(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector ограничение топ пользователей (максимум 10)."""
    now = datetime.now()

    # Создаем 15 пользователей
    users = [User(user_id=6000 + i, username=f"user{i}") for i in range(15)]
    clean_db_session.add_all(users)
    await clean_db_session.commit()

    # Создаем по одному сообщению от каждого
    messages = [
        Message(
            chat_id=6000 + i,
            user_id=6000 + i,
            role="user",
            content=f"Message {i}",
            content_length=10,
            created_at=now,
        )
        for i in range(15)
    ]
    clean_db_session.add_all(messages)
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)
    stats = await collector.get_statistics()

    assert stats.total_users == 15
    assert stats.active_users == 15
    assert len(stats.top_users) == 10  # Максимум 10


@pytest.mark.asyncio
async def test_real_stat_collector_custom_active_period(clean_db_session: AsyncSession) -> None:
    """Тест RealStatCollector с кастомным периодом активности."""
    now = datetime.now()

    # Создаем пользователя
    user = User(user_id=7001, username="user", first_name="User")
    clean_db_session.add(user)
    await clean_db_session.commit()

    # Создаем сообщение 45 дней назад
    message = Message(
        chat_id=7001,
        user_id=7001,
        role="user",
        content="Old message",
        content_length=11,
        created_at=now - timedelta(days=45),
    )
    clean_db_session.add(message)
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    # С периодом 30 дней - не активен
    collector_30 = RealStatCollector(session_factory=session_factory, active_users_days=30)
    stats_30 = await collector_30.get_statistics()
    assert stats_30.active_users == 0

    # С периодом 60 дней - активен
    collector_60 = RealStatCollector(session_factory=session_factory, active_users_days=60)
    stats_60 = await collector_60.get_statistics()
    assert stats_60.active_users == 1


@pytest.mark.asyncio
async def test_real_stat_collector_with_timezone_aware_datetime(
    clean_db_session: AsyncSession,
) -> None:
    """
    Тест RealStatCollector с timezone-aware datetime.

    Проверяет что RealStatCollector корректно работает с datetime,
    которые содержат timezone info (как это происходит в FastAPI).
    """
    now = datetime.now(UTC)

    # Создаем пользователя
    user = User(user_id=8001, username="user", first_name="User")
    clean_db_session.add(user)
    await clean_db_session.commit()

    # Создаем сообщения с разными датами
    # БД хранит TIMESTAMP WITHOUT TIME ZONE, поэтому сохраняем как naive
    messages = [
        Message(
            chat_id=8001,
            user_id=8001,
            role="user",
            content="Old message",
            content_length=11,
            created_at=(now - timedelta(days=10)).replace(tzinfo=None),
        ),
        Message(
            chat_id=8001,
            user_id=8001,
            role="user",
            content="Recent message",
            content_length=14,
            created_at=(now - timedelta(days=2)).replace(tzinfo=None),
        ),
    ]
    clean_db_session.add_all(messages)
    await clean_db_session.commit()

    async def session_factory():
        yield clean_db_session

    collector = RealStatCollector(session_factory=session_factory, active_users_days=30)

    # Тест с timezone-aware datetime (как в FastAPI)
    start_date_tz = now - timedelta(days=7)
    end_date_tz = now

    # Это должно работать без ошибок
    stats = await collector.get_statistics(start_date=start_date_tz, end_date=end_date_tz)

    assert stats.total_users == 1
    assert stats.active_users == 1
    assert stats.total_messages == 1  # Только сообщение за последние 7 дней
