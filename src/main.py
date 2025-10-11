import asyncio
import logging

from .bot import TelegramBot
from .config import Config
from .conversation import ConversationManager
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

    # Создание компонентов
    llm_client = LLMClient(config)
    conversation_manager = ConversationManager(max_history_messages=config.max_history_messages)

    # Создание бота
    bot = TelegramBot(config)

    # Регистрация handlers
    bot.dp.include_router(router)

    try:
        # Запуск polling с dependency injection
        await bot.dp.start_polling(
            bot.bot,
            llm_client=llm_client,
            conversation_manager=conversation_manager,
            system_prompt=config.system_prompt,
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
