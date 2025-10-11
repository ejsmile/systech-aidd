import logging

from .models import ConversationKey, Message

logger = logging.getLogger(__name__)


class ConversationManager:
    def __init__(self, max_history_messages: int = 20) -> None:
        self.max_history_messages: int = max_history_messages
        self.conversations: dict[ConversationKey, list[Message]] = {}

    def get_conversation_key(self, chat_id: int, user_id: int) -> ConversationKey:
        """Создать ключ диалога"""
        return ConversationKey(chat_id=chat_id, user_id=user_id)

    def add_message(self, key: ConversationKey, message: Message) -> None:
        """Добавить сообщение в историю"""
        if key not in self.conversations:
            self.conversations[key] = []

        self.conversations[key].append(message)

        # Ограничение истории (system prompt не учитываем)
        messages = self.conversations[key]
        non_system = [m for m in messages if m.role != "system"]
        if len(non_system) > self.max_history_messages:
            # Удаляем старые сообщения, сохраняя system prompt
            system_msgs = [m for m in messages if m.role == "system"]
            non_system = non_system[-self.max_history_messages :]
            self.conversations[key] = system_msgs + non_system

        logger.debug(f"Added message to conversation {key}, total: {len(self.conversations[key])}")

    def get_history(self, key: ConversationKey, system_prompt: str) -> list[Message]:
        """Получить историю диалога с system prompt"""
        if key not in self.conversations:
            self.conversations[key] = []

        # Убедимся, что system prompt всегда первый
        history = self.conversations[key]
        system_msgs = [m for m in history if m.role == "system"]

        if not system_msgs:
            # Добавляем system prompt, если его нет
            system_msg = Message(role="system", content=system_prompt)
            self.conversations[key].insert(0, system_msg)
            return self.conversations[key]

        return history

    def clear_history(self, key: ConversationKey) -> None:
        """Очистить историю диалога"""
        if key in self.conversations:
            del self.conversations[key]
            logger.info(f"Cleared conversation history for {key}")
