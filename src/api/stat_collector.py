"""Протокол для сборщиков статистики."""

from datetime import datetime
from typing import Protocol

from src.api.models import StatisticsResponse


class StatCollectorProtocol(Protocol):
    """
    Протокол для сборщиков статистики диалогов.

    Определяет интерфейс для получения статистики.
    Может иметь Mock и Real реализации.
    """

    async def get_statistics(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> StatisticsResponse:
        """
        Получить статистику по диалогам.

        Args:
            start_date: Начальная дата для фильтрации (опционально)
            end_date: Конечная дата для фильтрации (опционально)

        Returns:
            StatisticsResponse: Объект со статистикой
        """
        ...
