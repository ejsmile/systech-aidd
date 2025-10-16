from datetime import datetime

from sqlalchemy import BigInteger, Index, Integer, String, Text, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""

    pass


class Message(Base):
    """
    Модель сообщения в диалоге.

    Поддерживает soft delete через поле deleted_at.
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_length: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    deleted_at: Mapped[datetime | None] = mapped_column(nullable=True, default=None)

    __table_args__ = (
        # Основной индекс для быстрой выборки истории диалога
        Index(
            "idx_messages_lookup",
            "chat_id",
            "user_id",
            "deleted_at",
            "created_at",
            postgresql_ops={"created_at": "DESC"},
        ),
        # Индекс для сортировки по дате создания
        Index("idx_messages_created", "created_at", postgresql_ops={"created_at": "DESC"}),
    )

    def __repr__(self) -> str:
        return (
            f"<Message(id={self.id}, chat_id={self.chat_id}, "
            f"user_id={self.user_id}, role={self.role})>"
        )
