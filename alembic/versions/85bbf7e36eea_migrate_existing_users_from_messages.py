"""migrate existing users from messages

Revision ID: 85bbf7e36eea
Revises: 08c8618d6a0a
Create Date: 2025-10-16 16:50:43.370559

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "85bbf7e36eea"
down_revision: str | Sequence[str] | None = "08c8618d6a0a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Migrate existing users from messages table to users table."""
    # Извлечь уникальные user_id из messages и создать записи в users
    # с минимальными данными (username, first_name, last_name будут NULL)
    op.execute("""
        INSERT INTO users (user_id, username, first_name, last_name, created_at, updated_at)
        SELECT DISTINCT
            user_id,
            NULL as username,
            NULL as first_name,
            NULL as last_name,
            MIN(created_at) as created_at,
            CURRENT_TIMESTAMP as updated_at
        FROM messages
        WHERE deleted_at IS NULL
        GROUP BY user_id
        ON CONFLICT (user_id) DO NOTHING;
    """)


def downgrade() -> None:
    """Remove migrated users (those with NULL username, first_name, last_name)."""
    # Удаляем только пользователей, созданных через data-миграцию
    # (те, у которых все базовые поля NULL)
    op.execute("""
        DELETE FROM users
        WHERE username IS NULL AND first_name IS NULL AND last_name IS NULL;
    """)
