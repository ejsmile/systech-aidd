"""Seed test data

Revision ID: 9c0083885caf
Revises: 0b1d225cd32e
Create Date: 2025-10-16 15:00:18.228023

"""

from collections.abc import Sequence
from datetime import datetime, timedelta

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9c0083885caf"
down_revision: str | Sequence[str] | None = "0b1d225cd32e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Seed test data: 2 users with conversation history."""
    messages_table = sa.table(
        "messages",
        sa.column("chat_id", sa.BigInteger),
        sa.column("user_id", sa.BigInteger),
        sa.column("role", sa.String),
        sa.column("content", sa.Text),
        sa.column("content_length", sa.Integer),
        sa.column("created_at", sa.TIMESTAMP),
    )

    base_time = datetime.now() - timedelta(days=1)

    # Пользователь 1, Диалог 1 (chat_id=1001, user_id=101)
    user1_dialog1 = [
        {
            "chat_id": 1001,
            "user_id": 101,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": base_time,
        },
        {
            "chat_id": 1001,
            "user_id": 101,
            "role": "user",
            "content": "Привет! Как дела?",
            "content_length": 17,
            "created_at": base_time + timedelta(seconds=1),
        },
        {
            "chat_id": 1001,
            "user_id": 101,
            "role": "assistant",
            "content": "Здравствуйте! У меня всё отлично, спасибо! Чем могу помочь?",
            "content_length": 62,
            "created_at": base_time + timedelta(seconds=2),
        },
        {
            "chat_id": 1001,
            "user_id": 101,
            "role": "user",
            "content": "Расскажи про Python",
            "content_length": 19,
            "created_at": base_time + timedelta(seconds=5),
        },
        {
            "chat_id": 1001,
            "user_id": 101,
            "role": "assistant",
            "content": "Python - это высокоуровневый язык программирования, созданный Гвидо ван Россумом.",
            "content_length": 86,
            "created_at": base_time + timedelta(seconds=6),
        },
    ]

    # Пользователь 1, Диалог 2 (chat_id=1002, user_id=101)
    user1_dialog2 = [
        {
            "chat_id": 1002,
            "user_id": 101,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": base_time + timedelta(hours=1),
        },
        {
            "chat_id": 1002,
            "user_id": 101,
            "role": "user",
            "content": "Что такое Docker?",
            "content_length": 17,
            "created_at": base_time + timedelta(hours=1, seconds=1),
        },
        {
            "chat_id": 1002,
            "user_id": 101,
            "role": "assistant",
            "content": "Docker - это платформа для контейнеризации приложений.",
            "content_length": 56,
            "created_at": base_time + timedelta(hours=1, seconds=2),
        },
    ]

    # Пользователь 2, Диалог 1 (chat_id=2001, user_id=202)
    user2_dialog1 = [
        {
            "chat_id": 2001,
            "user_id": 202,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": base_time + timedelta(hours=2),
        },
        {
            "chat_id": 2001,
            "user_id": 202,
            "role": "user",
            "content": "Объясни что такое SQL",
            "content_length": 22,
            "created_at": base_time + timedelta(hours=2, seconds=1),
        },
        {
            "chat_id": 2001,
            "user_id": 202,
            "role": "assistant",
            "content": "SQL (Structured Query Language) - это язык структурированных запросов.",
            "content_length": 76,
            "created_at": base_time + timedelta(hours=2, seconds=2),
        },
        {
            "chat_id": 2001,
            "user_id": 202,
            "role": "user",
            "content": "А что такое NoSQL?",
            "content_length": 18,
            "created_at": base_time + timedelta(hours=2, seconds=5),
        },
        {
            "chat_id": 2001,
            "user_id": 202,
            "role": "assistant",
            "content": "NoSQL - это класс нереляционных баз данных.",
            "content_length": 47,
            "created_at": base_time + timedelta(hours=2, seconds=6),
        },
    ]

    # Пользователь 2, Диалог 2 (chat_id=2002, user_id=202)
    user2_dialog2 = [
        {
            "chat_id": 2002,
            "user_id": 202,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": base_time + timedelta(hours=3),
        },
        {
            "chat_id": 2002,
            "user_id": 202,
            "role": "user",
            "content": "Привет!",
            "content_length": 7,
            "created_at": base_time + timedelta(hours=3, seconds=1),
        },
        {
            "chat_id": 2002,
            "user_id": 202,
            "role": "assistant",
            "content": "Здравствуйте! Чем могу помочь?",
            "content_length": 31,
            "created_at": base_time + timedelta(hours=3, seconds=2),
        },
    ]

    # Вставка всех сообщений
    all_messages = user1_dialog1 + user1_dialog2 + user2_dialog1 + user2_dialog2
    op.bulk_insert(messages_table, all_messages)


def downgrade() -> None:
    """Remove test data."""
    # Удаляем все тестовые сообщения (по user_id 101 и 202)
    op.execute("DELETE FROM messages WHERE user_id IN (101, 202)")
