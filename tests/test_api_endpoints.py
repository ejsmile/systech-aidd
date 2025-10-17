"""Интеграционные тесты для API endpoints."""

from fastapi.testclient import TestClient

from src.api.app import app

client = TestClient(app)


def test_root_endpoint() -> None:
    """Тест корневого endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["version"] == "0.1.0"


def test_health_endpoint() -> None:
    """Тест health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_statistics_endpoint() -> None:
    """Тест основного endpoint статистики."""
    response = client.get("/api/v1/statistics")
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

    # Проверка значений
    assert data["total_users"] > 0
    assert data["active_users"] > 0
    assert data["total_messages"] > 0
    assert data["avg_messages_per_user"] >= 0


def test_statistics_endpoint_messages_by_date_structure() -> None:
    """Тест структуры messages_by_date."""
    response = client.get("/api/v1/statistics")
    assert response.status_code == 200

    data = response.json()
    messages_by_date = data["messages_by_date"]

    assert len(messages_by_date) > 0

    # Проверка структуры каждого элемента
    for item in messages_by_date:
        assert "date" in item
        assert "count" in item
        assert isinstance(item["count"], int)
        assert item["count"] >= 0


def test_statistics_endpoint_top_users_structure() -> None:
    """Тест структуры top_users."""
    response = client.get("/api/v1/statistics")
    assert response.status_code == 200

    data = response.json()
    top_users = data["top_users"]

    assert len(top_users) > 0
    assert len(top_users) <= 10  # Не больше 10

    # Проверка структуры каждого элемента
    for user in top_users:
        assert "user_id" in user
        assert "username" in user  # Может быть null
        assert "message_count" in user
        assert isinstance(user["user_id"], int)
        assert isinstance(user["message_count"], int)
        assert user["message_count"] > 0


def test_statistics_endpoint_with_date_params() -> None:
    """Тест endpoint с параметрами дат."""
    response = client.get(
        "/api/v1/statistics",
        params={
            "start_date": "2025-09-01T00:00:00",
            "end_date": "2025-10-17T23:59:59",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "total_users" in data
    assert data["total_users"] > 0


def test_statistics_endpoint_cors_headers() -> None:
    """Тест что CORS headers присутствуют при cross-origin запросе."""
    response = client.get(
        "/api/v1/statistics",
        headers={"Origin": "http://localhost:5173"},
    )
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_openapi_docs() -> None:
    """Тест что OpenAPI документация доступна."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    openapi = response.json()
    assert "openapi" in openapi
    assert "info" in openapi
    assert openapi["info"]["title"] == "AIDD API"


def test_statistics_consistency() -> None:
    """Тест что данные консистентны между вызовами."""
    response1 = client.get("/api/v1/statistics")
    response2 = client.get("/api/v1/statistics")

    assert response1.status_code == 200
    assert response2.status_code == 200

    data1 = response1.json()
    data2 = response2.json()

    # Mock данные должны быть идентичными
    assert data1["total_users"] == data2["total_users"]
    assert data1["active_users"] == data2["active_users"]
    assert data1["total_messages"] == data2["total_messages"]
