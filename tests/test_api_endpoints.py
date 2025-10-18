"""Интеграционные тесты для API endpoints."""

from collections.abc import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from src.api.app import app


@pytest.fixture
async def async_client(
    test_database_url: str, apply_migrations: None
) -> AsyncGenerator[AsyncClient, None]:
    """Async client для тестирования API с testcontainer."""
    from src.api.real_stat_collector import RealStatCollector  # noqa: PLC0415
    from src.database import Database  # noqa: PLC0415

    # Create fresh database instance for testing with testcontainer
    database = Database(test_database_url)

    # Initialize stat collector with test database
    stat_collector = RealStatCollector(
        session_factory=database.get_session,
        active_users_days=30,
    )

    # Override app dependencies
    import src.api.app as app_module  # noqa: PLC0415

    original_stat_collector = app_module.stat_collector
    app_module.stat_collector = stat_collector

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            yield client
    finally:
        # Restore original stat collector
        app_module.stat_collector = original_stat_collector
        await database.disconnect()


@pytest.mark.asyncio
async def test_root_endpoint(async_client: AsyncClient) -> None:
    """Тест корневого endpoint."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "0.1.0"


@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient) -> None:
    """Тест health check endpoint."""
    response = await async_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_statistics_endpoint(async_client: AsyncClient) -> None:
    """Тест основного endpoint статистики."""
    response = await async_client.get("/api/v1/statistics")
    assert response.status_code == 200

    data = response.json()

    # Проверка структуры ответа
    assert "total_users" in data
    assert "active_users" in data
    assert "total_messages" in data
    assert "avg_messages_per_user" in data
    assert "messages_by_date" in data
    assert "top_users" in data

    # Проверка типов данных
    assert isinstance(data["total_users"], int)
    assert isinstance(data["active_users"], int)
    assert isinstance(data["total_messages"], int)
    assert isinstance(data["avg_messages_per_user"], (int, float))
    assert isinstance(data["messages_by_date"], list)
    assert isinstance(data["top_users"], list)

    # Проверка значений (может быть 0 если БД пустая)
    assert data["total_users"] >= 0
    assert data["active_users"] >= 0
    assert data["total_messages"] >= 0
    assert data["avg_messages_per_user"] >= 0


@pytest.mark.asyncio
async def test_statistics_endpoint_messages_by_date_structure(async_client: AsyncClient) -> None:
    """Тест структуры messages_by_date."""
    response = await async_client.get("/api/v1/statistics")
    assert response.status_code == 200

    data = response.json()
    messages_by_date = data["messages_by_date"]

    # Может быть пустым если нет данных в БД
    if len(messages_by_date) > 0:
        # Проверка структуры каждого элемента
        for item in messages_by_date:
            assert "date" in item
            assert "count" in item
            assert isinstance(item["count"], int)
            assert item["count"] >= 0


@pytest.mark.asyncio
async def test_statistics_endpoint_top_users_structure(async_client: AsyncClient) -> None:
    """Тест структуры top_users."""
    response = await async_client.get("/api/v1/statistics")
    assert response.status_code == 200

    data = response.json()
    top_users = data["top_users"]

    # Может быть пустым если нет пользователей в БД
    assert len(top_users) <= 10  # Не больше 10

    # Проверка структуры каждого элемента если есть
    for user in top_users:
        assert "user_id" in user
        assert "username" in user  # Может быть null
        assert "message_count" in user
        assert isinstance(user["user_id"], int)
        assert isinstance(user["message_count"], int)
        assert user["message_count"] > 0


@pytest.mark.asyncio
async def test_statistics_endpoint_with_date_params(async_client: AsyncClient) -> None:
    """Тест endpoint с параметрами дат."""
    response = await async_client.get(
        "/api/v1/statistics",
        params={
            "start_date": "2025-09-01T00:00:00",
            "end_date": "2025-10-17T23:59:59",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "total_users" in data
    assert data["total_users"] >= 0


@pytest.mark.asyncio
async def test_statistics_endpoint_cors_headers(async_client: AsyncClient) -> None:
    """Тест что CORS headers присутствуют при cross-origin запросе."""
    response = await async_client.get(
        "/api/v1/statistics",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


@pytest.mark.asyncio
async def test_openapi_docs(async_client: AsyncClient) -> None:
    """Тест что OpenAPI документация доступна."""
    response = await async_client.get("/openapi.json")
    assert response.status_code == 200

    openapi = response.json()
    assert "openapi" in openapi
    assert "info" in openapi
    assert openapi["info"]["title"] == "AIDD API"


@pytest.mark.asyncio
async def test_statistics_consistency(async_client: AsyncClient) -> None:
    """Тест что данные консистентны между вызовами."""
    response1 = await async_client.get("/api/v1/statistics")
    response2 = await async_client.get("/api/v1/statistics")

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    # Данные должны быть идентичными (БД не меняется между запросами)
    assert data1["total_users"] == data2["total_users"]
    assert data1["active_users"] == data2["active_users"]
    assert data1["total_messages"] == data2["total_messages"]
