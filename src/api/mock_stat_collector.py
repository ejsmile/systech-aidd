"""Mock реализация сборщика статистики с фейковыми данными."""

import random
from datetime import datetime, timedelta
from typing import TypedDict

from src.api.models import MessageByDate, StatisticsResponse, TopUser

# Константы для генерации данных
_USERNAME_NULL_PROBABILITY = 0.2  # 20% пользователей без username
_ACTIVE_USERS_RATIO = 0.2  # 20% пользователей активные
_ACTIVE_MESSAGES_RATIO = 0.8  # 80% сообщений от активных пользователей


class _MockUser(TypedDict):
    """Внутренний тип для фейкового пользователя."""

    user_id: int
    username: str | None


class _MockMessage(TypedDict):
    """Внутренний тип для фейкового сообщения."""

    user_id: int
    created_at: datetime


class MockStatCollector:
    """
    Mock сборщик статистики с реалистичными фейковыми данными.

    Генерирует данные для разработки и тестирования frontend.
    """

    def __init__(self, num_users: int = 30, num_messages: int = 400, days_back: int = 30) -> None:
        """
        Инициализация Mock сборщика.

        Args:
            num_users: Количество фейковых пользователей (20-50)
            num_messages: Количество фейковых сообщений (200-500)
            days_back: Количество дней для распределения сообщений
        """
        self.num_users = num_users
        self.num_messages = num_messages
        self.days_back = days_back
        self._users = self._generate_users()
        self._messages = self._generate_messages()

    def _generate_users(self) -> list[_MockUser]:
        """Генерация фейковых пользователей."""
        usernames = [
            "john_doe",
            "jane_smith",
            "bob_wilson",
            "alice_brown",
            "charlie_davis",
            "diana_miller",
            "frank_moore",
            "grace_taylor",
            "henry_anderson",
            "ivy_thomas",
            "jack_jackson",
            "kate_white",
            "leo_harris",
            "mia_martin",
            "noah_garcia",
            "olivia_martinez",
            "peter_robinson",
            "quinn_clark",
            "ryan_rodriguez",
            "sara_lewis",
            "tom_lee",
            "uma_walker",
            "victor_hall",
            "wendy_allen",
            "xavier_young",
            "yara_king",
            "zack_wright",
            "anna_lopez",
            "ben_hill",
            "cara_scott",
        ]

        users: list[_MockUser] = []
        for i in range(self.num_users):
            user_id = 100000 + i
            # 20% пользователей без username
            username = (
                usernames[i]
                if i < len(usernames) and random.random() > _USERNAME_NULL_PROBABILITY
                else None
            )
            users.append(_MockUser(user_id=user_id, username=username))

        return users

    def _generate_messages(self) -> list[_MockMessage]:
        """Генерация фейковых сообщений с реалистичным распределением."""
        messages = []
        now = datetime.now()

        # Распределение активности пользователей (по закону Парето)
        # 20% пользователей создают 80% сообщений
        active_users_count = max(1, int(self.num_users * 0.2))
        active_users = random.sample(self._users, active_users_count)
        inactive_users = [u for u in self._users if u not in active_users]

        # 80% сообщений от активных пользователей
        active_messages_count = int(self.num_messages * 0.8)
        inactive_messages_count = self.num_messages - active_messages_count

        # Генерация сообщений от активных пользователей
        for _ in range(active_messages_count):
            user = random.choice(active_users)
            days_ago = random.randint(0, self.days_back - 1)
            created_at = now - timedelta(days=days_ago)
            messages.append(_MockMessage(user_id=user["user_id"], created_at=created_at))

        # Генерация сообщений от неактивных пользователей
        if inactive_users:
            for _ in range(inactive_messages_count):
                user = random.choice(inactive_users)
                days_ago = random.randint(0, self.days_back - 1)
                created_at = now - timedelta(days=days_ago)
                messages.append(_MockMessage(user_id=user["user_id"], created_at=created_at))

        return messages

    async def get_statistics(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> StatisticsResponse:
        """
        Получить фейковую статистику.

        Args:
            start_date: Начальная дата для фильтрации
            end_date: Конечная дата для фильтрации

        Returns:
            StatisticsResponse: Сгенерированная статистика
        """
        # Фильтрация сообщений по датам
        # Убираем timezone info для корректного сравнения
        filtered_messages = self._messages
        if start_date is not None:
            start_naive = start_date.replace(tzinfo=None) if start_date.tzinfo else start_date
            filtered_messages = [
                msg for msg in filtered_messages if msg["created_at"] >= start_naive
            ]
        if end_date is not None:
            end_naive = end_date.replace(tzinfo=None) if end_date.tzinfo else end_date
            filtered_messages = [msg for msg in filtered_messages if msg["created_at"] <= end_naive]

        # Подсчет статистики
        total_users = len(self._users)

        # Активные пользователи (с сообщениями в выбранном периоде)
        active_user_ids = {msg["user_id"] for msg in filtered_messages}
        active_users = len(active_user_ids)

        total_messages = len(filtered_messages)
        avg_messages_per_user = round(total_messages / active_users, 1) if active_users > 0 else 0.0

        # Группировка сообщений по датам (только отфильтрованные)
        messages_by_date_dict: dict[datetime, int] = {}
        for msg in filtered_messages:
            date = msg["created_at"].replace(hour=0, minute=0, second=0, microsecond=0)
            messages_by_date_dict[date] = messages_by_date_dict.get(date, 0) + 1

        messages_by_date = [
            MessageByDate(date=date, count=count)
            for date, count in sorted(messages_by_date_dict.items())
        ]

        # Топ пользователей по количеству сообщений (только отфильтрованные)
        user_message_counts: dict[int, int] = {}
        for msg in filtered_messages:
            user_id = msg["user_id"]
            user_message_counts[user_id] = user_message_counts.get(user_id, 0) + 1

        # Сортировка и выбор топ-10
        sorted_users = sorted(user_message_counts.items(), key=lambda x: x[1], reverse=True)[:10]

        top_users = []
        for user_id, message_count in sorted_users:
            user = next((u for u in self._users if u["user_id"] == user_id), None)
            if user:
                top_users.append(
                    TopUser(
                        user_id=user_id,
                        username=user["username"],
                        message_count=message_count,
                    )
                )

        return StatisticsResponse(
            total_users=total_users,
            active_users=active_users,
            total_messages=total_messages,
            avg_messages_per_user=avg_messages_per_user,
            messages_by_date=messages_by_date,
            top_users=top_users,
        )
