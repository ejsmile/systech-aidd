"""Тесты для Mock сборщика статистики."""

import pytest

from src.api.mock_stat_collector import MockStatCollector


@pytest.mark.asyncio
async def test_mock_stat_collector_basic() -> None:
    """Тест базовой работы MockStatCollector."""
    collector = MockStatCollector(num_users=20, num_messages=100)
    stats = await collector.get_statistics()

    assert stats.total_users == 20
    assert stats.active_users > 0
    assert stats.active_users <= stats.total_users
    assert stats.total_messages == 100
    assert stats.avg_messages_per_user >= 0


@pytest.mark.asyncio
async def test_mock_stat_collector_messages_by_date() -> None:
    """Тест распределения сообщений по датам."""
    collector = MockStatCollector(num_users=10, num_messages=50, days_back=7)
    stats = await collector.get_statistics()

    # Должны быть сообщения по датам
    assert len(stats.messages_by_date) > 0
    assert len(stats.messages_by_date) <= 7  # Не больше чем days_back

    # Все даты должны быть уникальными
    dates = [msg.date for msg in stats.messages_by_date]
    assert len(dates) == len(set(dates))

    # Даты должны быть отсортированы по возрастанию
    sorted_dates = sorted(dates)
    assert dates == sorted_dates

    # Сумма сообщений по датам должна равняться общему количеству
    total_by_date = sum(msg.count for msg in stats.messages_by_date)
    assert total_by_date == stats.total_messages


@pytest.mark.asyncio
async def test_mock_stat_collector_top_users() -> None:
    """Тест топ пользователей."""
    collector = MockStatCollector(num_users=30, num_messages=200)
    stats = await collector.get_statistics()

    # Должно быть не больше 10 топ пользователей
    assert len(stats.top_users) <= 10
    assert len(stats.top_users) > 0

    # Пользователи должны быть отсортированы по количеству сообщений (по убыванию)
    message_counts = [user.message_count for user in stats.top_users]
    assert message_counts == sorted(message_counts, reverse=True)

    # Все user_id должны быть уникальными
    user_ids = [user.user_id for user in stats.top_users]
    assert len(user_ids) == len(set(user_ids))

    # Все message_count должны быть положительными
    for user in stats.top_users:
        assert user.message_count > 0


@pytest.mark.asyncio
async def test_mock_stat_collector_avg_messages() -> None:
    """Тест расчета среднего количества сообщений."""
    collector = MockStatCollector(num_users=10, num_messages=100)
    stats = await collector.get_statistics()

    # Среднее должно быть положительным
    assert stats.avg_messages_per_user > 0

    # Среднее должно быть не больше общего количества сообщений
    assert stats.avg_messages_per_user <= stats.total_messages


@pytest.mark.asyncio
async def test_mock_stat_collector_active_users() -> None:
    """Тест подсчета активных пользователей."""
    collector = MockStatCollector(num_users=50, num_messages=500, days_back=30)
    stats = await collector.get_statistics()

    # Активные пользователи не должны превышать общее количество
    assert stats.active_users <= stats.total_users
    assert stats.active_users > 0


@pytest.mark.asyncio
async def test_mock_stat_collector_custom_params() -> None:
    """Тест с различными параметрами."""
    # Маленькие значения
    collector1 = MockStatCollector(num_users=5, num_messages=10)
    stats1 = await collector1.get_statistics()
    assert stats1.total_users == 5
    assert stats1.total_messages == 10

    # Большие значения
    collector2 = MockStatCollector(num_users=100, num_messages=1000)
    stats2 = await collector2.get_statistics()
    assert stats2.total_users == 100
    assert stats2.total_messages == 1000


@pytest.mark.asyncio
async def test_mock_stat_collector_username_nullable() -> None:
    """Тест что username может быть None."""
    collector = MockStatCollector(num_users=30, num_messages=200)
    stats = await collector.get_statistics()

    # Проверяем что есть пользователи с username и без
    usernames = [user.username for user in stats.top_users]
    # Хотя бы один пользователь должен быть
    assert len(usernames) > 0


@pytest.mark.asyncio
async def test_mock_stat_collector_consistency() -> None:
    """Тест что данные консистентны между вызовами."""
    collector = MockStatCollector(num_users=20, num_messages=100)

    stats1 = await collector.get_statistics()
    stats2 = await collector.get_statistics()

    # Данные должны быть одинаковыми (mock не меняется)
    assert stats1.total_users == stats2.total_users
    assert stats1.total_messages == stats2.total_messages
    assert len(stats1.top_users) == len(stats2.top_users)
