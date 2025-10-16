"""Общие fixtures для тестов"""

import asyncio
import os
from collections.abc import AsyncGenerator, Callable

import pytest
from alembic.config import Config as AlembicConfig
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource
from sqlalchemy.ext.asyncio import AsyncSession
from testcontainers.postgres import PostgresContainer

from alembic import command
from src.config import Config
from src.conversation import ConversationManager
from src.database import Database

# Отключаем Reaper для testcontainers (проблема на macOS)
os.environ["TESTCONTAINERS_RYUK_DISABLED"] = "true"


class ConfigForTests(Config):
    """Config для тестов - без загрузки .env файла и переменных окружения"""

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        # Используем только параметры инициализации, игнорируем .env и env переменные
        return (init_settings,)


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the entire test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def postgres_container():
    """Создать PostgreSQL контейнер для тестов"""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres


@pytest.fixture(scope="session")
async def test_database_url(postgres_container) -> str:
    """Получить URL тестовой базы данных"""
    return postgres_container.get_connection_url().replace("psycopg2", "asyncpg")


@pytest.fixture(scope="session")
async def apply_migrations(test_database_url: str) -> None:
    """Применить все миграции к тестовой БД"""
    # Устанавливаем URL для Alembic
    os.environ["DATABASE_URL"] = test_database_url

    # Настройка Alembic
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_database_url)

    # Применение миграций
    command.upgrade(alembic_cfg, "head")


@pytest.fixture
async def database(
    test_database_url: str, apply_migrations: None
) -> AsyncGenerator[Database, None]:
    """Создать подключение к тестовой БД"""
    db = Database(test_database_url)
    yield db
    await db.disconnect()


@pytest.fixture
async def db_session(database: Database) -> AsyncGenerator[AsyncSession, None]:
    """Создать сессию для работы с БД в тестах"""
    async for session in database.get_session():
        yield session


@pytest.fixture
async def session_factory(
    test_database_url: str, apply_migrations: None
) -> Callable[[], AsyncGenerator[AsyncSession, None]]:
    """Фабрика сессий для тестов"""
    db = Database(test_database_url)
    yield db.get_session
    await db.disconnect()


@pytest.fixture
async def conversation_manager(
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
) -> ConversationManager:
    """ConversationManager с настройками для тестов и подключением к БД"""
    return ConversationManager(session_factory=session_factory, max_history_messages=3)


@pytest.fixture
def mock_config() -> Config:
    """Минимальная валидная конфигурация для тестов"""
    return Config(
        telegram_token="test_token_123",
        openrouter_api_key="test_api_key_123",
    )
