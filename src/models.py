from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from aiogram.types import User


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


@dataclass(frozen=True)
class UserData:
    """
    Данные пользователя из Telegram Bot API.

    Используется для передачи данных между handlers и UserRepository.
    Immutable для предотвращения случайных изменений.
    """

    user_id: int
    username: str | None
    first_name: str | None
    last_name: str | None

    def to_dict(self) -> dict[str, int | str | None]:
        """Конвертация в dict для UserRepository"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }


def extract_user_data(telegram_user: "User") -> UserData:
    """
    Извлечь данные пользователя из Telegram User объекта.

    Args:
        telegram_user: Объект aiogram.types.User

    Returns:
        UserData с данными пользователя

    Note:
        username и last_name могут быть None если пользователь их не указал
    """
    return UserData(
        user_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
    )
