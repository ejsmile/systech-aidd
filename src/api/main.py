"""Точка входа для запуска FastAPI сервера."""

import logging

import uvicorn

# Импорт приложения для uvicorn
from src.api.app import app  # noqa: F401

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# Экспорт app для uvicorn
__all__ = ["app"]


def main() -> None:
    """Запуск FastAPI сервера."""
    logger.info("Starting AIDD API server...")

    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
