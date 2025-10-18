"""Тесты для Pydantic моделей API."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.api.models import MessageByDate, StatisticsResponse, TopUser


def test_message_by_date_valid() -> None:
    """Тест валидного объекта MessageByDate."""
    msg = MessageByDate(date=datetime(2025, 10, 17), count=42)
    assert msg.date == datetime(2025, 10, 17)
    assert msg.count == 42


def test_message_by_date_negative_count() -> None:
    """Тест что отрицательное количество сообщений недопустимо."""
    with pytest.raises(ValidationError):
        MessageByDate(date=datetime(2025, 10, 17), count=-1)


def test_top_user_valid() -> None:
    """Тест валидного объекта TopUser."""
    user = TopUser(user_id=123456, username="john_doe", message_count=100)
    assert user.user_id == 123456
    assert user.username == "john_doe"
    assert user.message_count == 100


def test_top_user_without_username() -> None:
    """Тест TopUser без username (None)."""
    user = TopUser(user_id=123456, username=None, message_count=50)
    assert user.user_id == 123456
    assert user.username is None
    assert user.message_count == 50


def test_top_user_negative_count() -> None:
    """Тест что отрицательное количество сообщений недопустимо."""
    with pytest.raises(ValidationError):
        TopUser(user_id=123456, username="test", message_count=-5)


def test_statistics_response_valid() -> None:
    """Тест валидного объекта StatisticsResponse."""
    stats = StatisticsResponse(
        total_users=100,
        active_users=50,
        total_messages=1000,
        avg_messages_per_user=20.0,
        messages_by_date=[
            MessageByDate(date=datetime(2025, 10, 17), count=50),
            MessageByDate(date=datetime(2025, 10, 18), count=75),
        ],
        top_users=[
            TopUser(user_id=1, username="user1", message_count=100),
            TopUser(user_id=2, username="user2", message_count=90),
        ],
    )
    assert stats.total_users == 100
    assert stats.active_users == 50
    assert stats.total_messages == 1000
    assert stats.avg_messages_per_user == 20.0
    assert len(stats.messages_by_date) == 2
    assert len(stats.top_users) == 2


def test_statistics_response_empty_lists() -> None:
    """Тест StatisticsResponse с пустыми списками."""
    stats = StatisticsResponse(
        total_users=0,
        active_users=0,
        total_messages=0,
        avg_messages_per_user=0.0,
        messages_by_date=[],
        top_users=[],
    )
    assert stats.total_users == 0
    assert len(stats.messages_by_date) == 0
    assert len(stats.top_users) == 0


def test_statistics_response_default_lists() -> None:
    """Тест StatisticsResponse с дефолтными значениями списков."""
    stats = StatisticsResponse(
        total_users=10,
        active_users=5,
        total_messages=50,
        avg_messages_per_user=10.0,
    )
    assert stats.messages_by_date == []
    assert stats.top_users == []


def test_statistics_response_negative_values() -> None:
    """Тест что отрицательные значения недопустимы."""
    with pytest.raises(ValidationError):
        StatisticsResponse(
            total_users=-1,
            active_users=0,
            total_messages=0,
            avg_messages_per_user=0.0,
        )


def test_statistics_response_json_serialization() -> None:
    """Тест JSON сериализации StatisticsResponse."""
    stats = StatisticsResponse(
        total_users=100,
        active_users=50,
        total_messages=1000,
        avg_messages_per_user=20.0,
        messages_by_date=[MessageByDate(date=datetime(2025, 10, 17), count=50)],
        top_users=[TopUser(user_id=1, username="test", message_count=100)],
    )
    json_data = stats.model_dump()
    assert json_data["total_users"] == 100
    assert json_data["active_users"] == 50
    assert len(json_data["messages_by_date"]) == 1
    assert len(json_data["top_users"]) == 1
