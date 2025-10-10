import asyncio
import logging
from .config import Config
from .bot import TelegramBot
from .handlers import router


def setup_logging(log_level: str):
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


async def main():
    # Загрузка конфигурации
    config = Config()
    
    # Настройка логирования
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting systech-aidd bot...")
    
    # Создание бота
    bot = TelegramBot(config)
    
    # Регистрация handlers
    bot.dp.include_router(router)
    
    try:
        # Запуск polling
        await bot.start_polling()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())

