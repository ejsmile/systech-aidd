import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from .llm_client import LLMClient
from .conversation import ConversationManager
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
async def cmd_clear(message: Message, conversation_manager: ConversationManager):
    logger.info(f"User {message.from_user.id} cleared conversation")
    key = conversation_manager.get_conversation_key(
        chat_id=message.chat.id,
        user_id=message.from_user.id
    )
    conversation_manager.clear_history(key)
    await message.answer("История диалога очищена")


@router.message()
async def handle_message(
    message: Message,
    llm_client: LLMClient,
    conversation_manager: ConversationManager,
    system_prompt: str
):
    """Обработка текстовых сообщений через LLM с историей"""
    logger.debug(f"User {message.from_user.id} sent: {message.text}")
    
    try:
        # Получаем ключ диалога
        key = conversation_manager.get_conversation_key(
            chat_id=message.chat.id,
            user_id=message.from_user.id
        )
        
        # Добавляем сообщение пользователя в историю
        user_message = LLMMessage(role="user", content=message.text)
        conversation_manager.add_message(key, user_message)
        
        # Получаем историю с system prompt
        history = conversation_manager.get_history(key, system_prompt)
        
        # Получение ответа от LLM
        response = await llm_client.get_response(history)
        
        # Добавляем ответ ассистента в историю
        assistant_message = LLMMessage(role="assistant", content=response)
        conversation_manager.add_message(key, assistant_message)
        
        # Отправка ответа пользователю
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await message.answer(
            "Произошла ошибка при обработке запроса. Попробуйте позже."
        )

