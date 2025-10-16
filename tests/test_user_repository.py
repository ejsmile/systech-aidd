"""Тесты для UserRepository"""

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.db_models import Message
from src.user_repository import UserRepository


class TestUserRepositoryUpsert:
    """Тесты для upsert_user"""

    async def test_upsert_creates_new_user(self, db_session: AsyncSession) -> None:
        """Тест создания нового пользователя"""
        repo = UserRepository(db_session)

        user = await repo.upsert_user(
            user_id=123456,  # noqa: PLR2004
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        assert user.user_id == 123456  # noqa: PLR2004
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.created_at is not None
        assert user.updated_at is not None

    async def test_upsert_updates_existing_user(self, db_session: AsyncSession) -> None:
        """Тест обновления существующего пользователя"""
        repo = UserRepository(db_session)

        # Создаем пользователя
        user1 = await repo.upsert_user(
            user_id=123456,  # noqa: PLR2004
            username="oldname",
            first_name="Old",
            last_name="Name",
        )
        created_at1 = user1.created_at

        # Обновляем пользователя
        user2 = await repo.upsert_user(
            user_id=123456,  # noqa: PLR2004
            username="newname",
            first_name="New",
            last_name="Name",
        )

        assert user2.user_id == 123456  # noqa: PLR2004
        assert user2.username == "newname"
        assert user2.first_name == "New"
        assert user2.last_name == "Name"
        assert user2.created_at == created_at1  # created_at не изменился
        assert user2.updated_at > created_at1  # updated_at обновился

    async def test_upsert_with_nullable_fields(self, db_session: AsyncSession) -> None:
        """Тест upsert с nullable полями"""
        repo = UserRepository(db_session)

        user = await repo.upsert_user(
            user_id=999888,  # noqa: PLR2004
            username=None,
            first_name="NoUsername",
            last_name=None,
        )

        assert user.user_id == 999888  # noqa: PLR2004
        assert user.username is None
        assert user.first_name == "NoUsername"
        assert user.last_name is None


class TestUserRepositoryGetById:
    """Тесты для get_user_by_id"""

    async def test_get_existing_user(self, db_session: AsyncSession) -> None:
        """Тест получения существующего пользователя"""
        repo = UserRepository(db_session)

        # Создаем пользователя
        await repo.upsert_user(
            user_id=555666,  # noqa: PLR2004
            username="testuser",
            first_name="Test",
        )

        # Получаем пользователя
        user = await repo.get_user_by_id(555666)  # noqa: PLR2004

        assert user is not None
        assert user.user_id == 555666  # noqa: PLR2004
        assert user.username == "testuser"

    async def test_get_nonexistent_user(self, db_session: AsyncSession) -> None:
        """Тест получения несуществующего пользователя"""
        repo = UserRepository(db_session)

        user = await repo.get_user_by_id(999999)  # noqa: PLR2004

        assert user is None


class TestUserRepositoryMessageCount:
    """Тесты для get_user_message_count"""

    async def test_message_count_with_messages(self, db_session: AsyncSession) -> None:
        """Тест подсчета сообщений для пользователя с сообщениями"""
        repo = UserRepository(db_session)

        # Создаем пользователя
        await repo.upsert_user(user_id=777888, username="testuser")  # noqa: PLR2004

        # Добавляем сообщения
        for i in range(5):  # noqa: PLR2004
            message = Message(
                chat_id=12345,  # noqa: PLR2004
                user_id=777888,  # noqa: PLR2004
                role="user",
                content=f"Test message {i}",
                content_length=10,  # noqa: PLR2004
            )
            db_session.add(message)
        await db_session.commit()

        # Проверяем количество
        count = await repo.get_user_message_count(777888)  # noqa: PLR2004

        assert count == 5  # noqa: PLR2004

    async def test_message_count_without_messages(self, db_session: AsyncSession) -> None:
        """Тест подсчета сообщений для пользователя без сообщений"""
        repo = UserRepository(db_session)

        count = await repo.get_user_message_count(999999)  # noqa: PLR2004

        assert count == 0

    async def test_message_count_ignores_deleted(self, db_session: AsyncSession) -> None:
        """Тест что подсчет игнорирует удаленные сообщения"""
        repo = UserRepository(db_session)

        # Создаем пользователя
        await repo.upsert_user(user_id=888999, username="testuser")  # noqa: PLR2004

        # Добавляем активные сообщения
        for i in range(3):  # noqa: PLR2004
            message = Message(
                chat_id=12345,  # noqa: PLR2004
                user_id=888999,  # noqa: PLR2004
                role="user",
                content=f"Active message {i}",
                content_length=10,  # noqa: PLR2004
            )
            db_session.add(message)

        # Добавляем удаленное сообщение
        deleted_message = Message(
            chat_id=12345,  # noqa: PLR2004
            user_id=888999,  # noqa: PLR2004
            role="user",
            content="Deleted message",
            content_length=10,  # noqa: PLR2004
        )
        deleted_message.deleted_at = datetime.now()
        db_session.add(deleted_message)

        await db_session.commit()

        # Проверяем что считаются только активные
        count = await repo.get_user_message_count(888999)  # noqa: PLR2004

        assert count == 3  # noqa: PLR2004
