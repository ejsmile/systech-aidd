import logging
from collections.abc import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from .models import ChatMessage, ConversationKey
from .repository import MessageRepository

logger = logging.getLogger(__name__)


class ConversationManager:
    """
    Управление историей диалогов с использованием базы данных.

    Использует MessageRepository для персистентного хранения.
    """

    def __init__(
        self,
        session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
        max_history_messages: int = 20,
    ) -> None:
        self.session_factory = session_factory
        self.max_history_messages: int = max_history_messages

    def get_conversation_key(self, chat_id: int, user_id: int) -> ConversationKey:
        """Создать ключ диалога"""
        return ConversationKey(chat_id=chat_id, user_id=user_id)

    async def add_message(self, key: ConversationKey, message: ChatMessage) -> None:
        """Добавить сообщение в историю (БД)"""
        session_gen = self.session_factory()
        session = await session_gen.__anext__()
        try:
            repo = MessageRepository(session)
            await repo.add_message(key, message)
        finally:
            await session_gen.aclose()

        logger.debug(f"Added message to conversation {key}")

    async def get_history(self, key: ConversationKey, system_prompt: str) -> list[ChatMessage]:
        """
        Получить историю диалога с system prompt.

        Если system prompt отсутствует в истории, он будет добавлен.
        System prompt всегда возвращается первым в списке.
        """
        session_gen = self.session_factory()
        session = await session_gen.__anext__()
        try:
            repo = MessageRepository(session)
            history = await repo.get_history(key, limit=self.max_history_messages)
        finally:
            await session_gen.aclose()

        # Проверяем наличие system prompt
        system_msgs = [m for m in history if m.role == "system"]

        if not system_msgs:
            # Добавляем system prompt, если его нет
            system_msg = ChatMessage(role="system", content=system_prompt)
            # Сохраняем в БД
            session_gen2 = self.session_factory()
            session2 = await session_gen2.__anext__()
            try:
                repo2 = MessageRepository(session2)
                await repo2.add_message(key, system_msg)
            finally:
                await session_gen2.aclose()

            logger.debug(f"Added system prompt to conversation {key}")
        else:
            system_msg = system_msgs[0]

        # Убираем system сообщения из истории и добавляем system_msg в начало
        non_system_history = [m for m in history if m.role != "system"]
        return [system_msg] + non_system_history

    async def clear_history(self, key: ConversationKey) -> None:
        """Очистить историю диалога (soft delete)"""
        session_gen = self.session_factory()
        session = await session_gen.__anext__()
        try:
            repo = MessageRepository(session)
            deleted_count = await repo.soft_delete_history(key)
        finally:
            await session_gen.aclose()

        logger.info(f"Cleared conversation history for {key}, deleted {deleted_count} messages")
