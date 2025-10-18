import logging
from collections.abc import AsyncGenerator, Callable

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from .conversation import ConversationManager
from .llm_client import LLMClient
from .models import ChatMessage, extract_user_data
from .user_repository import UserRepository

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    if message.from_user is None:
        return
    logger.info(f"User {message.from_user.id} started the bot")
    await message.answer(
        "Привет! Я LLM-ассистент.\n"
        "Просто отправь мне сообщение, и я отвечу.\n"
        "Используй /help для списка команд."
    )


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    if message.from_user is None:
        return
    logger.info(f"User {message.from_user.id} requested help")
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - показать справку\n"
        "/clear - очистить историю диалога\n"
        "/role - показать роль ассистента"
    )


@router.message(Command("clear"))
async def cmd_clear(message: Message, conversation_manager: ConversationManager) -> None:
    if message.from_user is None:
        return
    logger.info(f"User {message.from_user.id} cleared conversation")
    key = conversation_manager.get_conversation_key(
        chat_id=message.chat.id, user_id=message.from_user.id
    )
    await conversation_manager.clear_history(key)
    await message.answer("История диалога очищена")


@router.message(Command("role"))
async def cmd_role(message: Message, system_prompt: str) -> None:
    """Обработчик команды /role"""
    if message.from_user is None:
        return
    logger.info(f"User {message.from_user.id} requested role")
    await message.answer(f"Моя роль:\n\n{system_prompt}")


@router.message(F.text)
async def handle_message(
    message: Message,
    llm_client: LLMClient,
    conversation_manager: ConversationManager,
    session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
    system_prompt: str,
) -> None:
    """Обработка текстовых сообщений через LLM с историей"""
    if message.from_user is None or message.text is None:
        return
    logger.debug(f"User {message.from_user.id} sent: {message.text}")

    # Сохранить/обновить данные пользователя (с graceful degradation)
    try:
        user_data = extract_user_data(message.from_user)
        session_gen = session_factory()
        session = await session_gen.__anext__()
        try:
            user_repo = UserRepository(session)
            await user_repo.upsert_user(
                user_id=user_data.user_id,
                username=user_data.username,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
            )
            logger.debug(f"User data saved for user_id={user_data.user_id}")
        finally:
            await session_gen.aclose()
    except Exception as e:
        logger.error(f"Failed to save user data: {e}")
        # Продолжаем работу даже если сохранение не удалось

    try:
        # Получаем ключ диалога
        key = conversation_manager.get_conversation_key(
            chat_id=message.chat.id, user_id=message.from_user.id
        )

        # Добавляем сообщение пользователя в историю
        user_message = ChatMessage(role="user", content=message.text)
        await conversation_manager.add_message(key, user_message)

        # Получаем историю с system prompt
        history = await conversation_manager.get_history(key, system_prompt)

        # Получение ответа от LLM
        response = await llm_client.get_response(history)

        # Добавляем ответ ассистента в историю
        assistant_message = ChatMessage(role="assistant", content=response)
        await conversation_manager.add_message(key, assistant_message)

        # Отправка ответа пользователю
        await message.answer(response)

    except Exception as e:
        logger.error(f"Error processing message: {e}")
        await message.answer("Произошла ошибка при обработке запроса. Попробуйте позже.")


@router.message()
async def handle_unsupported(message: Message) -> None:
    """Обработка неподдерживаемых типов сообщений"""
    if message.from_user is None:
        return
    logger.warning(f"User {message.from_user.id} sent unsupported message type")
    # Тихо игнорируем - не отправляем ответ пользователю
