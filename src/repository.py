import logging
from datetime import datetime

from sqlalchemy import desc, select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from .db_models import Message
from .models import ChatMessage, ConversationKey

logger = logging.getLogger(__name__)


class MessageRepository:
    """Репозиторий для работы с сообщениями в базе данных"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_message(self, key: ConversationKey, message: ChatMessage) -> Message:
        """Добавить сообщение в БД"""
        content_length = len(message.content)
        db_message = Message(
            chat_id=key.chat_id,
            user_id=key.user_id,
            role=message.role,
            content=message.content,
            content_length=content_length,
        )
        self.session.add(db_message)
        await self.session.commit()
        await self.session.refresh(db_message)

        logger.debug(
            f"Added message to DB: chat_id={key.chat_id}, "
            f"user_id={key.user_id}, role={message.role}"
        )
        return db_message

    async def get_history(
        self, key: ConversationKey, limit: int | None = None
    ) -> list[ChatMessage]:
        """
        Получить историю диалога (только не удаленные сообщения).

        Args:
            key: Ключ диалога
            limit: Ограничение количества сообщений (кроме system)

        Returns:
            Список сообщений в формате ChatMessage
        """
        # Запрос всех не удаленных сообщений
        query = (
            select(Message)
            .where(
                Message.chat_id == key.chat_id,
                Message.user_id == key.user_id,
                Message.deleted_at.is_(None),
            )
            .order_by(desc(Message.created_at))
        )

        result = await self.session.execute(query)
        messages = list(result.scalars().all())

        # Разделяем system и не-system сообщения
        system_messages = [m for m in messages if m.role == "system"]
        non_system_messages = [m for m in messages if m.role != "system"]

        # Применяем лимит только к не-system сообщениям
        if limit is not None and len(non_system_messages) > limit:
            non_system_messages = non_system_messages[:limit]

        # Объединяем и сортируем по дате (от старых к новым)
        filtered_messages = system_messages + non_system_messages
        filtered_messages.sort(key=lambda m: m.created_at)

        # Конвертируем в ChatMessage
        chat_messages = [
            ChatMessage(role=msg.role, content=msg.content)  # type: ignore
            for msg in filtered_messages
        ]

        logger.debug(
            f"Retrieved {len(chat_messages)} messages from DB for "
            f"chat_id={key.chat_id}, user_id={key.user_id}"
        )
        return chat_messages

    async def soft_delete_history(self, key: ConversationKey) -> int:
        """
        Мягкое удаление всех сообщений диалога.

        Returns:
            Количество удаленных сообщений
        """
        query = (
            update(Message)
            .where(
                Message.chat_id == key.chat_id,
                Message.user_id == key.user_id,
                Message.deleted_at.is_(None),
            )
            .values(deleted_at=datetime.now())
        )

        result: CursorResult[tuple[int]] = await self.session.execute(query)  # type: ignore
        await self.session.commit()

        deleted_count: int = result.rowcount or 0
        logger.info(
            f"Soft deleted {deleted_count} messages for "
            f"chat_id={key.chat_id}, user_id={key.user_id}"
        )
        return deleted_count

    async def get_history_count(self, key: ConversationKey) -> int:
        """
        Получить количество не удаленных сообщений в диалоге.

        Returns:
            Количество сообщений
        """
        query = select(Message).where(
            Message.chat_id == key.chat_id,
            Message.user_id == key.user_id,
            Message.deleted_at.is_(None),
        )

        result = await self.session.execute(query)
        messages = result.scalars().all()
        count = len(list(messages))

        logger.debug(f"Message count for chat_id={key.chat_id}, user_id={key.user_id}: {count}")
        return count
