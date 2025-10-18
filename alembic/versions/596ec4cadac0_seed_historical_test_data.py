"""seed_historical_test_data

Revision ID: 596ec4cadac0
Revises: 85bbf7e36eea
Create Date: 2025-10-18 09:32:52.049908

"""

from collections.abc import Sequence
from datetime import datetime, timedelta

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "596ec4cadac0"
down_revision: str | Sequence[str] | None = "85bbf7e36eea"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Seed historical test data: messages from 1 and 2 months ago."""
    # Таблица users
    users_table = sa.table(
        "users",
        sa.column("user_id", sa.BigInteger),
        sa.column("username", sa.String),
        sa.column("first_name", sa.String),
        sa.column("last_name", sa.String),
        sa.column("bio", sa.Text),
        sa.column("age", sa.Integer),
        sa.column("created_at", sa.TIMESTAMP),
        sa.column("updated_at", sa.TIMESTAMP),
    )

    # Таблица messages
    messages_table = sa.table(
        "messages",
        sa.column("chat_id", sa.BigInteger),
        sa.column("user_id", sa.BigInteger),
        sa.column("role", sa.String),
        sa.column("content", sa.Text),
        sa.column("content_length", sa.Integer),
        sa.column("created_at", sa.TIMESTAMP),
    )

    # Базовые временные точки
    one_month_ago = datetime.now() - timedelta(days=30)
    two_months_ago = datetime.now() - timedelta(days=60)

    # ===== ПОЛЬЗОВАТЕЛИ =====
    users = [
        # Веб-пользователь - для веб-интерфейса
        {
            "user_id": 1,
            "username": "web-user-1",
            "first_name": "Web",
            "last_name": "User",
            "bio": "Web interface user for testing",
            "age": 25,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        },
        # Пользователь 3 - создан 2 месяца назад
        {
            "user_id": 301,
            "username": "history_user_1",
            "first_name": "Александр",
            "last_name": "Исторический",
            "bio": "Тестовый пользователь с историческими данными",
            "age": 25,
            "created_at": two_months_ago,
            "updated_at": two_months_ago,
        },
        # Пользователь 4 - создан месяц назад
        {
            "user_id": 401,
            "username": "history_user_2",
            "first_name": "Мария",
            "last_name": "Прошлая",
            "bio": "Еще один тестовый пользователь",
            "age": 30,
            "created_at": one_month_ago,
            "updated_at": one_month_ago,
        },
    ]

    # ===== ДИАЛОГИ 2 МЕСЯЦА НАЗАД =====
    # Пользователь 3, Диалог 1 (chat_id=3001, user_id=301)
    user3_dialog1_2m = [
        {
            "chat_id": 3001,
            "user_id": 301,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": two_months_ago,
        },
        {
            "chat_id": 3001,
            "user_id": 301,
            "role": "user",
            "content": "Привет! Расскажи про машинное обучение",
            "content_length": 40,
            "created_at": two_months_ago + timedelta(seconds=1),
        },
        {
            "chat_id": 3001,
            "user_id": 301,
            "role": "assistant",
            "content": "Машинное обучение - это раздел искусственного интеллекта, который изучает методы построения алгоритмов, способных обучаться.",
            "content_length": 134,
            "created_at": two_months_ago + timedelta(seconds=2),
        },
        {
            "chat_id": 3001,
            "user_id": 301,
            "role": "user",
            "content": "Какие бывают типы машинного обучения?",
            "content_length": 40,
            "created_at": two_months_ago + timedelta(seconds=5),
        },
        {
            "chat_id": 3001,
            "user_id": 301,
            "role": "assistant",
            "content": "Существуют три основных типа: обучение с учителем (supervised learning), обучение без учителя (unsupervised learning) и обучение с подкреплением (reinforcement learning).",
            "content_length": 179,
            "created_at": two_months_ago + timedelta(seconds=6),
        },
    ]

    # Пользователь 3, Диалог 2 (chat_id=3002, user_id=301) - через несколько часов
    user3_dialog2_2m = [
        {
            "chat_id": 3002,
            "user_id": 301,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": two_months_ago + timedelta(hours=3),
        },
        {
            "chat_id": 3002,
            "user_id": 301,
            "role": "user",
            "content": "Что такое нейронные сети?",
            "content_length": 26,
            "created_at": two_months_ago + timedelta(hours=3, seconds=1),
        },
        {
            "chat_id": 3002,
            "user_id": 301,
            "role": "assistant",
            "content": "Нейронные сети - это вычислительные модели, вдохновленные биологическими нейронными сетями в мозге. Они состоят из слоев взаимосвязанных узлов (нейронов).",
            "content_length": 161,
            "created_at": two_months_ago + timedelta(hours=3, seconds=2),
        },
        {
            "chat_id": 3002,
            "user_id": 301,
            "role": "user",
            "content": "Расскажи про глубокое обучение",
            "content_length": 31,
            "created_at": two_months_ago + timedelta(hours=3, seconds=5),
        },
        {
            "chat_id": 3002,
            "user_id": 301,
            "role": "assistant",
            "content": "Глубокое обучение (Deep Learning) - это подраздел машинного обучения, использующий многослойные нейронные сети. Оно особенно эффективно для обработки изображений, звука и текста.",
            "content_length": 191,
            "created_at": two_months_ago + timedelta(hours=3, seconds=6),
        },
    ]

    # ===== ДИАЛОГИ 1 МЕСЯЦ НАЗАД =====
    # Пользователь 4, Диалог 1 (chat_id=4001, user_id=401)
    user4_dialog1_1m = [
        {
            "chat_id": 4001,
            "user_id": 401,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": one_month_ago,
        },
        {
            "chat_id": 4001,
            "user_id": 401,
            "role": "user",
            "content": "Привет! Что такое DevOps?",
            "content_length": 26,
            "created_at": one_month_ago + timedelta(seconds=1),
        },
        {
            "chat_id": 4001,
            "user_id": 401,
            "role": "assistant",
            "content": "DevOps - это набор практик, объединяющих разработку (Development) и эксплуатацию (Operations) программного обеспечения. Цель - сократить цикл разработки и обеспечить непрерывную доставку.",
            "content_length": 198,
            "created_at": one_month_ago + timedelta(seconds=2),
        },
        {
            "chat_id": 4001,
            "user_id": 401,
            "role": "user",
            "content": "Какие инструменты используются в DevOps?",
            "content_length": 42,
            "created_at": one_month_ago + timedelta(seconds=5),
        },
        {
            "chat_id": 4001,
            "user_id": 401,
            "role": "assistant",
            "content": "Основные инструменты: Docker и Kubernetes для контейнеризации, Jenkins и GitLab CI для CI/CD, Terraform для инфраструктуры как кода, Prometheus и Grafana для мониторинга.",
            "content_length": 185,
            "created_at": one_month_ago + timedelta(seconds=6),
        },
    ]

    # Пользователь 4, Диалог 2 (chat_id=4002, user_id=401) - через несколько дней
    user4_dialog2_1m = [
        {
            "chat_id": 4002,
            "user_id": 401,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": one_month_ago + timedelta(days=3),
        },
        {
            "chat_id": 4002,
            "user_id": 401,
            "role": "user",
            "content": "Расскажи про микросервисную архитектуру",
            "content_length": 40,
            "created_at": one_month_ago + timedelta(days=3, seconds=1),
        },
        {
            "chat_id": 4002,
            "user_id": 401,
            "role": "assistant",
            "content": "Микросервисная архитектура - это подход к разработке приложения как набора небольших независимых сервисов, каждый из которых работает в собственном процессе и взаимодействует через легковесные механизмы.",
            "content_length": 209,
            "created_at": one_month_ago + timedelta(days=3, seconds=2),
        },
    ]

    # Пользователь 3, дополнительный диалог 1 месяц назад (chat_id=3003, user_id=301)
    user3_dialog3_1m = [
        {
            "chat_id": 3003,
            "user_id": 301,
            "role": "system",
            "content": "Ты полезный ассистент.",
            "content_length": 25,
            "created_at": one_month_ago + timedelta(days=5),
        },
        {
            "chat_id": 3003,
            "user_id": 301,
            "role": "user",
            "content": "Что такое трансформеры в ML?",
            "content_length": 29,
            "created_at": one_month_ago + timedelta(days=5, seconds=1),
        },
        {
            "chat_id": 3003,
            "user_id": 301,
            "role": "assistant",
            "content": "Трансформеры - это архитектура нейронных сетей, основанная на механизме внимания (attention mechanism). Они революционизировали обработку естественного языка и лежат в основе моделей типа GPT и BERT.",
            "content_length": 200,
            "created_at": one_month_ago + timedelta(days=5, seconds=2),
        },
        {
            "chat_id": 3003,
            "user_id": 301,
            "role": "user",
            "content": "Как работает механизм внимания?",
            "content_length": 32,
            "created_at": one_month_ago + timedelta(days=5, seconds=5),
        },
        {
            "chat_id": 3003,
            "user_id": 301,
            "role": "assistant",
            "content": "Механизм внимания позволяет модели фокусироваться на разных частях входных данных при обработке каждого элемента. Это помогает улавливать долгосрочные зависимости в последовательностях.",
            "content_length": 184,
            "created_at": one_month_ago + timedelta(days=5, seconds=6),
        },
    ]

    # Вставка пользователей
    op.bulk_insert(users_table, users)

    # Вставка всех сообщений
    all_messages = (
        user3_dialog1_2m + user3_dialog2_2m + user4_dialog1_1m + user4_dialog2_1m + user3_dialog3_1m
    )
    op.bulk_insert(messages_table, all_messages)


def downgrade() -> None:
    """Remove historical test data."""
    # Удаляем тестовые сообщения
    op.execute("DELETE FROM messages WHERE user_id IN (1, 301, 401)")
    # Удаляем тестовых пользователей
    op.execute("DELETE FROM users WHERE user_id IN (1, 301, 401)")
