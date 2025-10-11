from dataclasses import dataclass


@dataclass(frozen=True)
class ConversationKey:
    """Immutable ключ для идентификации диалога"""

    chat_id: int
    user_id: int


@dataclass
class Message:
    role: str  # "system", "user", или "assistant"
    content: str

    def to_dict(self) -> dict[str, str]:
        """Конвертация в формат OpenAI API"""
        return {"role": self.role, "content": self.content}
