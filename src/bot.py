import logging

from aiogram import Bot, Dispatcher

from .config import Config

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.bot: Bot = Bot(token=config.telegram_token)
        self.dp: Dispatcher = Dispatcher()

    async def stop(self) -> None:
        logger.info("Stopping bot...")
        await self.bot.session.close()
