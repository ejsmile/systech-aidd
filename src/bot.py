import logging
from aiogram import Bot, Dispatcher
from .config import Config

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, config: Config):
        self.config = config
        self.bot = Bot(token=config.telegram_token)
        self.dp = Dispatcher()
    
    async def start_polling(self):
        logger.info("Starting bot polling...")
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        logger.info("Stopping bot...")
        await self.bot.session.close()

