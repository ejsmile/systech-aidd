from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Role(str, Enum):
    """Роли участников диалога"""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class ConversationKey:
    """
    Immutable ключ для идентификации диалога.

    Комбинация chat_id + user_id позволяет различать пользователей
    в групповых чатах и приватных диалогах.
    """

    chat_id: int
    user_id: int


@dataclass
class ChatMessage:
    """
    Сообщение в диалоге с LLM.

    Формат совместим с OpenAI Chat Completions API.
    """

    role: Literal["system", "user", "assistant"]
    content: str

    def to_dict(self) -> dict[str, str]:
        """Конвертация в формат OpenAI API"""
        return {"role": self.role, "content": self.content}
