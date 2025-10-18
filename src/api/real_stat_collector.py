"""Real реализация сборщика статистики на основе PostgreSQL."""

from collections.abc import AsyncGenerator, Callable
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import MessageByDate, StatisticsResponse, TopUser
from src.db_models import Message, User


def _to_naive_datetime(dt: datetime | None) -> datetime | None:
    """
    Конвертировать datetime в naive (без timezone).

    PostgreSQL колонки TIMESTAMP WITHOUT TIME ZONE требуют naive datetime.
    """
    if dt is None:
        return None
    if dt.tzinfo is not None:
        # Конвертируем в UTC и убираем timezone info
        return dt.replace(tzinfo=None)
    return dt


class RealStatCollector:
    """
    Real сборщик статистики из PostgreSQL.

    Получает реальные данные из таблиц users и messages.
    """

    def __init__(
        self,
        session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
        active_users_days: int = 30,
    ) -> None:
        """
        Инициализация Real сборщика.

        Args:
            session_factory: Фабрика для создания database session
            active_users_days: Период в днях для определения активных пользователей
        """
        self.session_factory = session_factory
        self.active_users_days = active_users_days

    async def get_statistics(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> StatisticsResponse:
        """
        Получить статистику из PostgreSQL.

        Args:
            start_date: Начальная дата для фильтрации (опционально)
            end_date: Конечная дата для фильтрации (опционально)

        Returns:
            StatisticsResponse: Статистика по пользователям и сообщениям
        """
        # Если даты не указаны, используем период active_users_days
        if start_date is None and end_date is None:
            start_date = datetime.now() - timedelta(days=self.active_users_days)

        # Конвертируем datetime в naive (БД использует TIMESTAMP WITHOUT TIME ZONE)
        start_date = _to_naive_datetime(start_date)
        end_date = _to_naive_datetime(end_date)

        async for session in self.session_factory():
            # Total users
            total_users = await self._get_total_users(session)

            # Active users (пользователи с сообщениями за период)
            active_users = await self._get_active_users(session, start_date, end_date)

            # Total messages (с фильтрацией по датам и deleted_at)
            total_messages = await self._get_total_messages(session, start_date, end_date)

            # Average messages per user
            avg_messages_per_user = (
                round(total_messages / active_users, 1) if active_users > 0 else 0.0
            )

            # Messages by date
            messages_by_date = await self._get_messages_by_date(session, start_date, end_date)

            # Top users
            top_users = await self._get_top_users(session, start_date, end_date)

            return StatisticsResponse(
                total_users=total_users,
                active_users=active_users,
                total_messages=total_messages,
                avg_messages_per_user=avg_messages_per_user,
                messages_by_date=messages_by_date,
                top_users=top_users,
            )

        # Этот код никогда не должен выполняться, но нужен для mypy
        raise RuntimeError("Session factory didn't yield a session")

    async def _get_total_users(self, session: AsyncSession) -> int:
        """Получить общее количество пользователей."""
        result = await session.execute(select(func.count(User.user_id)))
        return result.scalar() or 0

    async def _get_active_users(
        self,
        session: AsyncSession,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> int:
        """
        Получить количество активных пользователей.

        Активные - пользователи с сообщениями за указанный период.
        """
        query = select(func.count(func.distinct(Message.user_id))).where(
            Message.deleted_at.is_(None)
        )

        if start_date is not None:
            query = query.where(Message.created_at >= start_date)
        if end_date is not None:
            query = query.where(Message.created_at <= end_date)

        result = await session.execute(query)
        return result.scalar() or 0

    async def _get_total_messages(
        self,
        session: AsyncSession,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> int:
        """Получить общее количество сообщений (не удаленных)."""
        query = select(func.count(Message.id)).where(Message.deleted_at.is_(None))

        if start_date is not None:
            query = query.where(Message.created_at >= start_date)
        if end_date is not None:
            query = query.where(Message.created_at <= end_date)

        result = await session.execute(query)
        return result.scalar() or 0

    async def _get_messages_by_date(
        self,
        session: AsyncSession,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[MessageByDate]:
        """Получить распределение сообщений по датам."""
        # Группировка по дате (без времени)
        date_column = func.date(Message.created_at)

        query = (
            select(date_column.label("date"), func.count(Message.id).label("count"))
            .where(Message.deleted_at.is_(None))
            .group_by(date_column)
            .order_by(date_column)
        )

        if start_date is not None:
            query = query.where(Message.created_at >= start_date)
        if end_date is not None:
            query = query.where(Message.created_at <= end_date)

        result = await session.execute(query)
        rows = result.all()

        return [
            MessageByDate(
                date=datetime.combine(row.date, datetime.min.time()),
                count=row.count,  # type: ignore[arg-type]
            )
            for row in rows
        ]

    async def _get_top_users(
        self,
        session: AsyncSession,
        start_date: datetime | None,
        end_date: datetime | None,
    ) -> list[TopUser]:
        """Получить топ-10 пользователей по количеству сообщений."""
        # Подсчет сообщений по пользователям
        query = (
            select(
                Message.user_id,
                func.count(Message.id).label("message_count"),
            )
            .where(Message.deleted_at.is_(None))
            .group_by(Message.user_id)
            .order_by(func.count(Message.id).desc())
            .limit(10)
        )

        if start_date is not None:
            query = query.where(Message.created_at >= start_date)
        if end_date is not None:
            query = query.where(Message.created_at <= end_date)

        result = await session.execute(query)
        rows = result.all()

        # Получить username для каждого пользователя
        top_users = []
        for row in rows:
            user_result = await session.execute(
                select(User.username).where(User.user_id == row.user_id)
            )
            username = user_result.scalar_one_or_none()

            top_users.append(
                TopUser(
                    user_id=row.user_id,
                    username=username,
                    message_count=row.message_count,
                )
            )

        return top_users
