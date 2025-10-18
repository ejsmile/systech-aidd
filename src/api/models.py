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


class ChatMessageRequest(BaseModel):
    """Запрос на отправку сообщения в чат."""

    user_id: str = Field(description="ID веб-пользователя (например, 'web-user-1')")
    message: str = Field(min_length=1, max_length=4000, description="Текст сообщения")


class ChatMessageResponse(BaseModel):
    """Ответ на сообщение в чате."""

    response: str = Field(description="Ответ бота")
    message_id: int = Field(description="ID сохраненного сообщения")


class ChatHistoryItem(BaseModel):
    """Элемент истории чата."""

    role: str = Field(description="Роль: system, user или assistant")
    content: str = Field(description="Содержимое сообщения")
    created_at: datetime = Field(description="Время создания сообщения")


class ChatHistoryResponse(BaseModel):
    """История чата пользователя."""

    messages: list[ChatHistoryItem] = Field(default_factory=list, description="Список сообщений")


class ClearHistoryResponse(BaseModel):
    """Результат очистки истории."""

    success: bool = Field(description="Успешно ли выполнена очистка")
    deleted_count: int = Field(ge=0, description="Количество удаленных сообщений")


class Text2SQLRequest(BaseModel):
    """Запрос для Text2SQL обработки."""

    query: str = Field(description="Вопрос на естественном языке")


class Text2SQLResponse(BaseModel):
    """Ответ с SQL запросом и результатами."""

    sql: str = Field(description="Сгенерированный SQL запрос")
    result: list[dict[str, object]] = Field(description="Результат выполнения")
    interpretation: str = Field(description="Интерпретация результата")
