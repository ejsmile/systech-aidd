"""Тесты для моделей базы данных"""

from src.db_models import Message, User


class TestMessageModel:
    """Тесты для модели Message"""

    def test_message_repr(self) -> None:
        """Тест строкового представления модели Message"""
        message = Message(
            id=1,
            chat_id=123,
            user_id=456,
            role="user",
            content="Test message",
            content_length=12,
        )

        repr_str = repr(message)
        assert "Message(" in repr_str
        assert "id=1" in repr_str
        assert "chat_id=123" in repr_str
        assert "user_id=456" in repr_str
        assert "role=user" in repr_str


class TestUserModel:
    """Тесты для модели User"""

    def test_user_model_creation(self) -> None:
        """Тест создания модели User с обязательными полями"""
        user = User(
            user_id=123456789,  # noqa: PLR2004
            username="testuser",
            first_name="Test",
            last_name="User",
        )

        assert user.user_id == 123456789  # noqa: PLR2004
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.bio is None
        assert user.age is None

    def test_user_model_with_nullable_fields(self) -> None:
        """Тест создания модели User с nullable полями"""
        user = User(
            user_id=987654321,  # noqa: PLR2004
            username=None,
            first_name="NoUsername",
            last_name=None,
        )

        assert user.user_id == 987654321  # noqa: PLR2004
        assert user.username is None
        assert user.first_name == "NoUsername"
        assert user.last_name is None

    def test_user_model_minimal(self) -> None:
        """Тест создания модели User только с user_id"""
        user = User(
            user_id=111222333,  # noqa: PLR2004
            username=None,
            first_name=None,
            last_name=None,
        )

        assert user.user_id == 111222333  # noqa: PLR2004
        assert user.username is None
        assert user.first_name is None
        assert user.last_name is None
        assert user.bio is None
        assert user.age is None

    def test_user_model_with_optional_fields(self) -> None:
        """Тест создания модели User со всеми опциональными полями"""
        user = User(
            user_id=555666777,  # noqa: PLR2004
            username="fulluser",
            first_name="Full",
            last_name="Name",
            bio="Test bio description",
            age=25,  # noqa: PLR2004
        )

        assert user.user_id == 555666777  # noqa: PLR2004
        assert user.username == "fulluser"
        assert user.first_name == "Full"
        assert user.last_name == "Name"
        assert user.bio == "Test bio description"
        assert user.age == 25  # noqa: PLR2004

    def test_user_repr(self) -> None:
        """Тест строкового представления модели User"""
        user = User(
            user_id=123456789,  # noqa: PLR2004
            username="testuser",
            first_name="Test",
        )

        repr_str = repr(user)
        assert "User(" in repr_str
        assert "user_id=123456789" in repr_str
        assert "username=testuser" in repr_str
        assert "first_name=Test" in repr_str

    def test_user_repr_without_username(self) -> None:
        """Тест строкового представления модели User без username"""
        user = User(
            user_id=999888777,  # noqa: PLR2004
            username=None,
            first_name="NoUsername",
        )

        repr_str = repr(user)
        assert "User(" in repr_str
        assert "user_id=999888777" in repr_str
        assert "username=None" in repr_str
        assert "first_name=NoUsername" in repr_str
