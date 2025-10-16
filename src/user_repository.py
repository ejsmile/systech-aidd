"""Репозиторий для работы с пользователями в базе данных"""

import logging
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import Message, User

logger = logging.getLogger(__name__)


class UserRepository:
    """Репозиторий для работы с пользователями в базе данных"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def upsert_user(
        self,
        user_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> User:
        """
        Создать или обновить пользователя (UPSERT).

        При конфликте по user_id обновляет username, first_name, last_name, updated_at.

        Args:
            user_id: ID пользователя в Telegram
            username: Username пользователя (без @)
            first_name: Имя пользователя
            last_name: Фамилия пользователя

        Returns:
            Объект User из БД
        """
        stmt = insert(User).values(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # При конфликте обновляем данные
        stmt = stmt.on_conflict_do_update(
            index_elements=["user_id"],
            set_={
                "username": stmt.excluded.username,
                "first_name": stmt.excluded.first_name,
                "last_name": stmt.excluded.last_name,
                "updated_at": datetime.now(),
            },
        )

        await self.session.execute(stmt)
        await self.session.commit()

        # Получаем созданного/обновленного пользователя
        result = await self.session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one()

        # Обновляем объект из БД чтобы получить актуальные данные
        await self.session.refresh(user)

        logger.info(f"Upserted user: user_id={user_id}, username={username}")
        return user

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Получить пользователя по ID.

        Args:
            user_id: ID пользователя в Telegram

        Returns:
            Объект User или None если не найден
        """
        result = await self.session.execute(select(User).where(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if user:
            logger.debug(f"Found user: user_id={user_id}")
        else:
            logger.debug(f"User not found: user_id={user_id}")

        return user

    async def get_user_message_count(self, user_id: int) -> int:
        """
        Получить количество сообщений пользователя.

        Args:
            user_id: ID пользователя в Telegram

        Returns:
            Количество не удаленных сообщений
        """
        result = await self.session.execute(
            select(func.count(Message.id)).where(
                Message.user_id == user_id,
                Message.deleted_at.is_(None),
            )
        )
        count = result.scalar() or 0

        logger.debug(f"Message count for user_id={user_id}: {count}")
        return count
