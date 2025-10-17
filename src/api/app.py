"""FastAPI приложение для веб-интерфейса."""

from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from src.api.mock_stat_collector import MockStatCollector
from src.api.models import StatisticsResponse
from src.api.stat_collector import StatCollectorProtocol

# Создание FastAPI приложения
app = FastAPI(
    title="AIDD API",
    description="API для дашборда и веб-чата AIDD бота",
    version="0.1.0",
)

# Настройка CORS для frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:3000",  # React/Next.js default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Глобальный экземпляр сборщика статистики (Mock версия)
stat_collector: StatCollectorProtocol = MockStatCollector(
    num_users=30, num_messages=400, days_back=30
)


@app.get("/")
async def root() -> dict[str, str]:
    """Корневой endpoint."""
    return {"message": "AIDD API is running", "version": "0.1.0"}


@app.get("/api/v1/statistics", response_model=StatisticsResponse)
async def get_statistics(
    start_date: Annotated[datetime | None, Query(description="Начальная дата (ISO format)")] = None,
    end_date: Annotated[datetime | None, Query(description="Конечная дата (ISO format)")] = None,
) -> StatisticsResponse:
    """
    Получить статистику диалогов для дашборда.

    Args:
        start_date: Начальная дата для фильтрации (опционально)
        end_date: Конечная дата для фильтрации (опционально)

    Returns:
        StatisticsResponse: Статистика по пользователям и сообщениям
    """
    return await stat_collector.get_statistics(start_date=start_date, end_date=end_date)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
