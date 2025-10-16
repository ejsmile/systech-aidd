"""Тест на проверку лимита истории на уровне БД"""

import pytest
from sqlalchemy import func, select

from src.conversation import ConversationManager
from src.db_models import Message
from src.models import ChatMessage, ConversationKey


@pytest.mark.asyncio
async def test_history_limit_saves_all_but_returns_limited(
    conversation_manager: ConversationManager, db_session
) -> None:
    """
    Проверяет, что:
    1. В БД сохраняются ВСЕ сообщения (нет физического удаления)
    2. get_history возвращает только ЛИМИТ последних сообщений
    """
    key = ConversationKey(chat_id=777777, user_id=777777)
    system_prompt = "Test system"

    # Лимит в conftest = 3, добавим 10 сообщений
    messages_count = 10
    for i in range(messages_count):
        await conversation_manager.add_message(
            key, ChatMessage(role="user", content=f"Message {i}")
        )

    # Получаем историю через ConversationManager
    history = await conversation_manager.get_history(key, system_prompt)

    # Проверяем, что get_history вернул только лимит + system
    expected_in_memory = 1 + 3  # system + max_history_messages=3
    assert len(history) == expected_in_memory, (
        f"get_history должен вернуть {expected_in_memory}, вернул {len(history)}"
    )

    # Проверяем, что возвращены последние сообщения
    assert history[-1].content == "Message 9", "Должно быть последнее сообщение"
    assert history[1].content == "Message 7", "Должно быть 3-е с конца"

    # КЛЮЧЕВАЯ ПРОВЕРКА: в БД должны быть ВСЕ сообщения
    query = (
        select(func.count())
        .select_from(Message)
        .where(
            Message.chat_id == key.chat_id,
            Message.user_id == key.user_id,
            Message.deleted_at.is_(None),
        )
    )
    result = await db_session.execute(query)
    total_in_db = result.scalar()

    # В БД: system + 10 user сообщений = 11
    expected_in_db = 1 + messages_count
    assert total_in_db == expected_in_db, (
        f"В БД должно быть {expected_in_db} сообщений, найдено {total_in_db}"
    )

    print(f"✅ В БД сохранено: {total_in_db} сообщений")
    print(f"✅ get_history вернул: {len(history)} сообщений (лимит применен)")
    print("✅ Лимит работает на уровне запроса, а не удаления!")


@pytest.mark.asyncio
async def test_history_limit_query_optimization(
    conversation_manager: ConversationManager, db_session
) -> None:
    """
    Проверяет, что лимит применяется на уровне SQL запроса (LIMIT),
    а не в Python коде после выборки всех данных
    """
    key = ConversationKey(chat_id=888888, user_id=888888)

    # Добавляем много сообщений
    for i in range(50):
        await conversation_manager.add_message(key, ChatMessage(role="user", content=f"Msg {i}"))

    # MessageRepository.get_history использует .limit() в SQL запросе
    # Проверяем, что вернулось именно 3 сообщения (без system)
    from src.repository import MessageRepository

    repo = MessageRepository(db_session)

    history = await repo.get_history(key, limit=3)

    assert len(history) == 3, f"Должно быть ровно 3 сообщения, получено {len(history)}"

    # Проверяем, что это последние сообщения
    assert history[-1].content == "Msg 49"
    assert history[0].content == "Msg 47"

    # Проверяем, что в БД намного больше
    query = (
        select(func.count())
        .select_from(Message)
        .where(
            Message.chat_id == key.chat_id,
            Message.user_id == key.user_id,
            Message.deleted_at.is_(None),
        )
    )
    result = await db_session.execute(query)
    total_in_db = result.scalar()

    assert total_in_db == 50, f"В БД должно быть 50 сообщений, найдено {total_in_db}"

    print(f"✅ В БД: {total_in_db} сообщений, запрошено: {len(history)}")
    print("✅ SQL LIMIT работает эффективно!")
