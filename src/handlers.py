import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from .llm_client import LLMClient
from .models import Message as LLMMessage

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


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    logger.info(f"User {message.from_user.id} cleared conversation")
    await message.answer("История диалога очищена")


@router.message()
async def handle_message(message: Message, llm_client: LLMClient, system_prompt: str):
    """Обработка текстовых сообщений через LLM"""
    logger.debug(f"User {message.from_user.id} sent: {message.text}")
    
    try:
        # Формирование запроса к LLM
        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=message.text),
        ]
        
        # Получение ответа от LLM
        response = await llm_client.get_response(messages)
        
        # Отправка ответа пользователю
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await message.answer(
            "Произошла ошибка при обработке запроса. Попробуйте позже."
        )

