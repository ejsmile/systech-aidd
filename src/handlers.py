import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "Привет! Я LLM-ассистент.\n"
        "Просто отправь мне сообщение, и я отвечу.\n"
        "Используй /help для списка команд."
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - показать справку\n"
        "/clear - очистить историю диалога"
    )


@router.message()
async def echo_message(message: Message):
    logger.debug(f"User {message.from_user.id} sent: {message.text}")
    await message.answer(message.text)

