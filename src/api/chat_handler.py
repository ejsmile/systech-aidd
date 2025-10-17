import logging

from src.api.models import ChatHistoryItem, ChatHistoryResponse
from src.conversation import ConversationManager
from src.llm_client import LLMClient
from src.models import ChatMessage

logger = logging.getLogger(__name__)


def user_id_to_int(user_id: str) -> int:
    """Convert string user_id to integer for ConversationKey."""
    return hash(user_id) % (2**31)


class WebChatHandler:
    """Обработчик веб-чата (аналог Telegram handlers)."""

    def __init__(
        self,
        llm_client: LLMClient,
        conversation_manager: ConversationManager,
        system_prompt: str,
    ) -> None:
        self.llm_client: LLMClient = llm_client
        self.conversation_manager: ConversationManager = conversation_manager
        self.system_prompt: str = system_prompt

    async def send_message(self, user_id: str, message: str) -> tuple[str, int]:
        """
        Отправить сообщение и получить ответ.

        Args:
            user_id: ID веб-пользователя (строка)
            message: Текст сообщения пользователя

        Returns:
            Кортеж (ответ от бота, ID сохраненного сообщения)
        """
        # Преобразование user_id в int
        user_id_int = user_id_to_int(user_id)
        key = self.conversation_manager.get_conversation_key(
            chat_id=user_id_int, user_id=user_id_int
        )

        try:
            # Добавляем сообщение пользователя в историю
            user_message = ChatMessage(role="user", content=message)
            await self.conversation_manager.add_message(key, user_message)

            # Получаем историю с system prompt
            history = await self.conversation_manager.get_history(key, self.system_prompt)

            # Получение ответа от LLM
            response = await self.llm_client.get_response(history)

            # Добавляем ответ ассистента в историю
            assistant_message = ChatMessage(role="assistant", content=response)
            await self.conversation_manager.add_message(key, assistant_message)

            logger.debug(f"Chat message processed for user {user_id}")

            # TODO: Получить message_id последнего сохраненного сообщения из БД
            message_id = 0  # Placeholder

            return response, message_id

        except Exception as e:
            logger.error(f"Error processing chat message for user {user_id}: {e}")
            raise

    async def get_history(self, user_id: str) -> ChatHistoryResponse:
        """
        Получить историю чата.

        Args:
            user_id: ID веб-пользователя

        Returns:
            ChatHistoryResponse с списком сообщений (без system сообщений)
        """
        user_id_int = user_id_to_int(user_id)
        key = self.conversation_manager.get_conversation_key(
            chat_id=user_id_int, user_id=user_id_int
        )

        try:
            # Получаем историю
            history = await self.conversation_manager.get_history(key, self.system_prompt)

            # Фильтруем system сообщения для отправки клиенту
            client_history = [
                ChatHistoryItem(
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at
                    if hasattr(msg, "created_at")
                    else __import__("datetime").datetime.now(),
                )
                for msg in history
                if msg.role != "system"
            ]

            logger.debug(f"History retrieved for user {user_id}")
            return ChatHistoryResponse(messages=client_history)

        except Exception as e:
            logger.error(f"Error retrieving history for user {user_id}: {e}")
            raise

    async def clear_history(self, user_id: str) -> int:
        """
        Очистить историю чата.

        Args:
            user_id: ID веб-пользователя

        Returns:
            Количество удаленных сообщений
        """
        user_id_int = user_id_to_int(user_id)
        key = self.conversation_manager.get_conversation_key(
            chat_id=user_id_int, user_id=user_id_int
        )

        try:
            await self.conversation_manager.clear_history(key)
            logger.info(f"History cleared for user {user_id}")
            return 0  # TODO: Return actual deleted count from repository

        except Exception as e:
            logger.error(f"Error clearing history for user {user_id}: {e}")
            raise
