"""Интеграционные тесты для работы с пользователями

Проверяет полный цикл работы с данными пользователей:
- Получение данных из Telegram
- Сохранение в БД через UserRepository
- Обновление существующих пользователей
- Взаимодействие с MessageRepository
"""

import asyncio
from collections.abc import AsyncGenerator, Callable
from datetime import datetime
from unittest.mock import Mock

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db_models import User
from src.models import ChatMessage, ConversationKey, extract_user_data
from src.repository import MessageRepository
from src.user_repository import UserRepository


@pytest.mark.asyncio
async def test_full_user_lifecycle_new_user(
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> None:
    """
    Тест полного цикла для НОВОГО пользователя:
    Telegram User → extract_user_data → UserRepository.upsert → DB → get_user_by_id
    """
    # 1. Мокируем Telegram User (новый пользователь)
    telegram_user = Mock()
    telegram_user.id = 999888777  # noqa: PLR2004
    telegram_user.username = "newuser"
    telegram_user.first_name = "New"
    telegram_user.last_name = "User"

    # 2. Извлекаем данные
    user_data = extract_user_data(telegram_user)

    assert user_data.user_id == 999888777  # noqa: PLR2004
    assert user_data.username == "newuser"
    assert user_data.first_name == "New"
    assert user_data.last_name == "User"

    # 3. Сохраняем в БД через UserRepository
    session_gen = session_factory()
    session = await session_gen.__anext__()
    try:
        repo = UserRepository(session)
        created_user = await repo.upsert_user(**user_data.to_dict())

        assert created_user.user_id == 999888777  # noqa: PLR2004
        assert created_user.username == "newuser"
        assert created_user.first_name == "New"
        assert created_user.last_name == "User"
        assert created_user.created_at is not None
        assert created_user.updated_at is not None

        # 4. Проверяем что пользователь действительно в БД
        fetched_user = await repo.get_user_by_id(999888777)  # noqa: PLR2004

        assert fetched_user is not None
        assert fetched_user.user_id == 999888777  # noqa: PLR2004
        assert fetched_user.username == "newuser"
        assert fetched_user.first_name == "New"
        assert fetched_user.last_name == "User"
    finally:
        await session_gen.aclose()


@pytest.mark.asyncio
async def test_user_migration_scenario(
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> None:
    """
    Тест сценария МИГРАЦИИ:
    1. Создать пользователя с минимальными данными (как после data-миграции)
    2. Вызвать upsert с полными данными из Telegram
    3. Проверить что данные обновились
    """
    session_gen = session_factory()
    session = await session_gen.__anext__()
    try:
        # 1. Создаём пользователя с минимальными данными (имитация миграции)
        migrated_user = User(
            user_id=111222333,  # noqa: PLR2004
            username=None,
            first_name=None,
            last_name=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        session.add(migrated_user)
        await session.commit()

        # Проверяем что пользователь создан с NULL полями
        stmt = select(User).where(User.user_id == 111222333)  # noqa: PLR2004
        result = await session.execute(stmt)
        user_before = result.scalar_one()

        assert user_before.username is None
        assert user_before.first_name is None
        assert user_before.last_name is None

        # Небольшая задержка чтобы updated_at точно изменился
        await asyncio.sleep(0.01)

        # 2. Мокируем Telegram User с полными данными
        telegram_user = Mock()
        telegram_user.id = 111222333  # noqa: PLR2004
        telegram_user.username = "migrated_user"
        telegram_user.first_name = "Migrated"
        telegram_user.last_name = "User"

        user_data = extract_user_data(telegram_user)

        # 3. Обновляем через upsert
        repo = UserRepository(session)
        updated_user = await repo.upsert_user(**user_data.to_dict())

        # 4. Проверяем что данные обновились
        assert updated_user.user_id == 111222333  # noqa: PLR2004
        assert updated_user.username == "migrated_user"
        assert updated_user.first_name == "Migrated"
        assert updated_user.last_name == "User"

        # Проверяем что updated_at изменился
        assert updated_user.updated_at >= user_before.updated_at

        # Проверяем что created_at НЕ изменился (сохранена оригинальная дата)
        # (используем округление до секунды, т.к. могут быть микросекундные различия)
        assert abs((updated_user.created_at - user_before.created_at).total_seconds()) < 1
    finally:
        await session_gen.aclose()


@pytest.mark.asyncio
async def test_user_update_on_repeated_interaction(
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> None:
    """
    Тест обновления данных пользователя при повторном взаимодействии:
    Пользователь меняет username → данные обновляются в БД
    """
    session_gen = session_factory()
    session = await session_gen.__anext__()
    try:
        repo = UserRepository(session)

        # 1. Первое взаимодействие
        user1 = await repo.upsert_user(
            user_id=444555666,  # noqa: PLR2004
            username="oldname",
            first_name="John",
            last_name="Doe",
        )

        assert user1.username == "oldname"
        first_updated_at = user1.updated_at

        # 2. Пользователь меняет username (второе взаимодействие)
        user2 = await repo.upsert_user(
            user_id=444555666,  # noqa: PLR2004
            username="newname",
            first_name="John",
            last_name="Smith",  # Также меняет фамилию
        )

        assert user2.username == "newname"
        assert user2.first_name == "John"
        assert user2.last_name == "Smith"
        assert user2.updated_at > first_updated_at

        # 3. Проверяем что в БД только одна запись
        fetched_user = await repo.get_user_by_id(444555666)  # noqa: PLR2004
        assert fetched_user is not None
        assert fetched_user.username == "newname"
        assert fetched_user.last_name == "Smith"
    finally:
        await session_gen.aclose()


@pytest.mark.asyncio
async def test_user_repository_with_message_repository(
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> None:
    """
    Тест взаимодействия UserRepository + MessageRepository:
    Проверяем что количество сообщений пользователя корректно подсчитывается
    """
    session_gen = session_factory()
    session = await session_gen.__anext__()
    try:
        user_repo = UserRepository(session)
        msg_repo = MessageRepository(session)

        # 1. Создаём пользователя
        user = await user_repo.upsert_user(
            user_id=777888999,  # noqa: PLR2004
            username="testmsg",
            first_name="Test",
            last_name="Msg",
        )

        # 2. Проверяем что сообщений пока нет
        count_before = await user_repo.get_user_message_count(user.user_id)
        assert count_before == 0

        # 3. Добавляем несколько сообщений
        key = ConversationKey(chat_id=12345, user_id=user.user_id)  # noqa: PLR2004
        await msg_repo.add_message(key, ChatMessage(role="user", content="Message 1"))
        await msg_repo.add_message(key, ChatMessage(role="assistant", content="Response 1"))
        await msg_repo.add_message(key, ChatMessage(role="user", content="Message 2"))

        # 4. Проверяем что количество сообщений увеличилось
        count_after = await user_repo.get_user_message_count(user.user_id)
        assert count_after == 3  # noqa: PLR2004

        # 5. Soft-delete всех сообщений
        deleted_count = await msg_repo.soft_delete_history(key)
        assert deleted_count == 3  # noqa: PLR2004

        # 6. Проверяем что deleted сообщения не учитываются
        count_after_delete = await user_repo.get_user_message_count(user.user_id)
        assert count_after_delete == 0
    finally:
        await session_gen.aclose()


@pytest.mark.asyncio
async def test_user_with_nullable_fields(
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> None:
    """
    Тест создания пользователя с NULL полями (username, last_name могут быть None):
    Некоторые пользователи Telegram не указывают username или фамилию
    """
    session_gen = session_factory()
    session = await session_gen.__anext__()
    try:
        repo = UserRepository(session)

        # Создаём пользователя без username и last_name
        user = await repo.upsert_user(
            user_id=123456789,  # noqa: PLR2004
            username=None,
            first_name="OnlyFirst",
            last_name=None,
        )

        assert user.user_id == 123456789  # noqa: PLR2004
        assert user.username is None
        assert user.first_name == "OnlyFirst"
        assert user.last_name is None

        # Проверяем что пользователь доступен через get_by_id
        fetched = await repo.get_user_by_id(123456789)  # noqa: PLR2004
        assert fetched is not None
        assert fetched.username is None
        assert fetched.last_name is None
    finally:
        await session_gen.aclose()


@pytest.mark.asyncio
async def test_extract_user_data_with_telegram_mock(
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> None:
    """
    Интеграционный тест для extract_user_data:
    Проверяем что данные корректно извлекаются и сохраняются в БД
    """
    # 1. Мокируем Telegram User без username
    telegram_user = Mock()
    telegram_user.id = 987654321  # noqa: PLR2004
    telegram_user.username = None  # Пользователь не указал username
    telegram_user.first_name = "Anonymous"
    telegram_user.last_name = "User"

    # 2. Извлекаем данные
    user_data = extract_user_data(telegram_user)

    assert user_data.user_id == 987654321  # noqa: PLR2004
    assert user_data.username is None
    assert user_data.first_name == "Anonymous"
    assert user_data.last_name == "User"

    # 3. Сохраняем в БД
    session_gen = session_factory()
    session = await session_gen.__anext__()
    try:
        repo = UserRepository(session)
        saved_user = await repo.upsert_user(**user_data.to_dict())

        assert saved_user.user_id == 987654321  # noqa: PLR2004
        assert saved_user.username is None
        assert saved_user.first_name == "Anonymous"
    finally:
        await session_gen.aclose()
