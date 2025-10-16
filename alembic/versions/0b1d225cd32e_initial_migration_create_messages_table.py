"""Initial migration: create messages table

Revision ID: 0b1d225cd32e
Revises:
Create Date: 2025-10-16 14:59:47.739885

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0b1d225cd32e"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # Создание таблицы messages
    op.create_table(
        "messages",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_length", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("deleted_at", sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # Создание индексов
    op.create_index(
        "idx_messages_lookup",
        "messages",
        ["chat_id", "user_id", "deleted_at", sa.text("created_at DESC")],
        unique=False,
    )
    op.create_index(
        "idx_messages_created",
        "messages",
        [sa.text("created_at DESC")],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Удаление индексов
    op.drop_index("idx_messages_created", table_name="messages")
    op.drop_index("idx_messages_lookup", table_name="messages")

    # Удаление таблицы
    op.drop_table("messages")
