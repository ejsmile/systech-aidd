"""Pydantic модели для API ответов."""

from datetime import datetime

from pydantic import BaseModel, Field


class MessageByDate(BaseModel):
    """Количество сообщений по дате."""

    date: datetime = Field(description="Дата (без времени)")
    count: int = Field(ge=0, description="Количество сообщений за день")


class TopUser(BaseModel):
    """Информация о топ пользователе."""

    user_id: int = Field(description="Telegram ID пользователя")
    username: str | None = Field(default=None, description="Telegram username")
    message_count: int = Field(ge=0, description="Количество сообщений пользователя")


class StatisticsResponse(BaseModel):
    """Ответ с полной статистикой для дашборда."""

    total_users: int = Field(ge=0, description="Общее количество пользователей")
    active_users: int = Field(ge=0, description="Активные пользователи (за 30 дней)")
    total_messages: int = Field(ge=0, description="Общее количество сообщений")
    avg_messages_per_user: float = Field(ge=0, description="Среднее сообщений на пользователя")
    messages_by_date: list[MessageByDate] = Field(
        default_factory=list, description="Распределение сообщений по датам"
    )
    top_users: list[TopUser] = Field(
        default_factory=list, description="Топ-10 активных пользователей"
    )
