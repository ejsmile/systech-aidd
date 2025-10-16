import asyncio
import logging

from .bot import TelegramBot
from .config import Config, load_system_prompt_with_fallback
from .conversation import ConversationManager
from .database import Database
from .handlers import router
from .llm_client import LLMClient


def setup_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


async def main() -> None:
    # Загрузка конфигурации
    config = Config()  # type: ignore[call-arg]

    # Настройка логирования
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting systech-aidd bot...")

    # Инициализация базы данных
    database = Database(config.database_url)

    # Проверка подключения к БД
    if not await database.check_connection():
        logger.error("Failed to connect to database. Exiting...")
        return

    logger.info("Database connection successful")

    # Загрузка системного промпта из файла (с fallback на дефолт)
    system_prompt = load_system_prompt_with_fallback(config.system_prompt_file)
    logger.info(f"System prompt loaded from {config.system_prompt_file}")

    # Создание компонентов
    llm_client = LLMClient(config)
    conversation_manager = ConversationManager(
        session_factory=database.get_session,
        max_history_messages=config.max_history_messages,
    )

    # Создание бота
    bot = TelegramBot(config)

    # Регистрация handlers
    bot.dp.include_router(router)

    try:
        # Запуск polling с dependency injection
        logger.info("Starting bot polling...")
        await bot.dp.start_polling(
            bot.bot,
            llm_client=llm_client,
            conversation_manager=conversation_manager,
            system_prompt=system_prompt,
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        logger.info("Shutting down...")
        await bot.stop()
        await database.disconnect()
        logger.info("Bot shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())
