"""FastAPI приложение для веб-интерфейса."""

from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from src.api.chat_handler import WebChatHandler
from src.api.mock_stat_collector import MockStatCollector
from src.api.models import (
    ChatHistoryResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    ClearHistoryResponse,
    StatisticsResponse,
    Text2SQLRequest,
    Text2SQLResponse,
)
from src.api.stat_collector import StatCollectorProtocol
from src.api.text2sql_handler import Text2SQLHandler
from src.config import Config
from src.conversation import ConversationManager
from src.database import Database
from src.llm_client import LLMClient

# Создание FastAPI приложения
app = FastAPI(
    title="AIDD API",
    description="API для дашборда и веб-чата AIDD бота",
    version="0.1.0",
)

# Настройка CORS для frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default
        "http://localhost:5174",  # Vite alternative port
        "http://localhost:3000",  # React/Next.js default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Глобальный экземпляр сборщика статистики (Mock версия)
stat_collector: StatCollectorProtocol = MockStatCollector(
    num_users=30, num_messages=400, days_back=30
)

# Инициализация зависимостей для чата
config = Config()  # type: ignore[call-arg]

# Try to initialize database, but handle gracefully if it fails
database: Database | None = None
chat_handler: WebChatHandler | None = None
try:
    database = Database(config.database_url)
    llm_client = LLMClient(config)
    conversation_manager = ConversationManager(
        session_factory=database.get_session,
        max_history_messages=config.max_history_messages,
    )
    chat_handler = WebChatHandler(
        llm_client=llm_client,
        conversation_manager=conversation_manager,
        system_prompt=config.system_prompt,
    )
except Exception as e:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(f"Failed to initialize database: {e}. Chat endpoints will not work.")

# Load Text2SQL prompt
try:
    with open("prompts/text2sql.txt", encoding="utf-8") as f:
        text2sql_prompt = f.read().strip()
except FileNotFoundError:
    text2sql_prompt = "Generate SQL queries for the given questions."

text2sql_handler: Text2SQLHandler | None = None
try:
    if database is not None:
        text2sql_handler = Text2SQLHandler(
            llm_client=llm_client,
            session_factory=database.get_session,
            text2sql_prompt=text2sql_prompt,
        )
except Exception as e:
    import logging

    logger = logging.getLogger(__name__)
    logger.warning(f"Failed to initialize Text2SQL handler: {e}")


@app.get("/")
async def root() -> dict[str, str]:
    """Корневой endpoint."""
    return {"message": "AIDD API is running", "version": "0.1.0"}


@app.get("/api/v1/statistics", response_model=StatisticsResponse)
async def get_statistics(
    start_date: Annotated[datetime | None, Query(description="Начальная дата (ISO format)")] = None,
    end_date: Annotated[datetime | None, Query(description="Конечная дата (ISO format)")] = None,
) -> StatisticsResponse:
    """
    Получить статистику диалогов для дашборда.

    Args:
        start_date: Начальная дата для фильтрации (опционально)
        end_date: Конечная дата для фильтрации (опционально)

    Returns:
        StatisticsResponse: Статистика по пользователям и сообщениям
    """
    return await stat_collector.get_statistics(start_date=start_date, end_date=end_date)


@app.post("/api/v1/chat/message", response_model=ChatMessageResponse)
async def send_chat_message(request: ChatMessageRequest) -> ChatMessageResponse:
    """
    Отправить сообщение в чат и получить ответ от бота.

    Args:
        request: ChatMessageRequest с user_id и сообщением

    Returns:
        ChatMessageResponse с ответом бота и message_id
    """
    if chat_handler is None:
        raise RuntimeError("Chat handler not initialized")
    response, message_id = await chat_handler.send_message(
        user_id=request.user_id, message=request.message
    )
    return ChatMessageResponse(response=response, message_id=message_id)


@app.get("/api/v1/chat/history/{user_id}", response_model=ChatHistoryResponse)
async def get_chat_history(user_id: str) -> ChatHistoryResponse:
    """
    Получить историю чата пользователя.

    Args:
        user_id: ID веб-пользователя

    Returns:
        ChatHistoryResponse с историей сообщений
    """
    if chat_handler is None:
        raise RuntimeError("Chat handler not initialized")
    return await chat_handler.get_history(user_id=user_id)


@app.delete("/api/v1/chat/history/{user_id}", response_model=ClearHistoryResponse)
async def clear_chat_history(user_id: str) -> ClearHistoryResponse:
    """
    Очистить историю чата пользователя.

    Args:
        user_id: ID веб-пользователя

    Returns:
        ClearHistoryResponse с результатом очистки
    """
    if chat_handler is None:
        raise RuntimeError("Chat handler not initialized")
    deleted_count = await chat_handler.clear_history(user_id=user_id)
    return ClearHistoryResponse(success=True, deleted_count=deleted_count)


@app.post("/api/v1/admin/query", response_model=Text2SQLResponse)
async def execute_admin_query(request: Text2SQLRequest) -> Text2SQLResponse:
    """
    Выполнить Text2SQL запрос (админ функция).

    Args:
        request: Text2SQLRequest с вопросом на естественном языке

    Returns:
        Text2SQLResponse с SQL запросом, результатом и интерпретацией
    """
    if text2sql_handler is None:
        raise RuntimeError("Text2SQL handler not initialized")

    try:
        return await text2sql_handler.process_query(user_query=request.query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
