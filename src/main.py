import asyncio
import logging
from .config import Config
from .bot import TelegramBot
from .llm_client import LLMClient
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
    
    # Создание LLM клиента
    llm_client = LLMClient(config)
    
    # Создание бота
    bot = TelegramBot(config)
    
    # Регистрация handlers
    bot.dp.include_router(router)
    
    try:
        # Запуск polling с dependency injection
        await bot.dp.start_polling(
            bot.bot,
            llm_client=llm_client,
            system_prompt=config.system_prompt,
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())

