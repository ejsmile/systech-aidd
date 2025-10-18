import logging
import re
from collections.abc import AsyncGenerator, Callable

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import Text2SQLResponse
from src.llm_client import LLMClient
from src.models import ChatMessage

logger = logging.getLogger(__name__)

# SQL whitelist for security
ALLOWED_TABLES = {"users", "messages"}
FORBIDDEN_KEYWORDS = {"DELETE", "UPDATE", "DROP", "ALTER", "CREATE", "INSERT"}


class Text2SQLHandler:
    """Обработчик Text2SQL запросов для администратора."""

    def __init__(
        self,
        llm_client: LLMClient,
        session_factory: Callable[[], AsyncGenerator[AsyncSession, None]],
        text2sql_prompt: str,
    ) -> None:
        self.llm_client: LLMClient = llm_client
        self.session_factory: Callable[[], AsyncGenerator[AsyncSession, None]] = session_factory
        self.text2sql_prompt: str = text2sql_prompt

    def validate_sql(self, sql: str) -> bool:
        """Валидация SQL: только SELECT, whitelist таблиц."""
        # Remove markdown code fence markers
        cleaned = re.sub(r"```\s*sql\s*", "", sql)
        cleaned = re.sub(r"```\s*", "", cleaned)

        # Remove comments and extra whitespace
        cleaned = re.sub(r"--.*$", "", cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r"/\*.*?\*/", "", cleaned, flags=re.DOTALL)
        cleaned = cleaned.strip()

        # Check if it starts with SELECT (case insensitive)
        if not re.match(r"^\s*SELECT\b", cleaned, re.IGNORECASE):
            logger.warning(f"SQL validation failed: not a SELECT query: {sql}")
            return False

        # Check for forbidden keywords
        for keyword in FORBIDDEN_KEYWORDS:
            if re.search(rf"\b{keyword}\b", cleaned, re.IGNORECASE):
                logger.warning(f"SQL validation failed: forbidden keyword {keyword} in: {sql}")
                return False

        # Check that only whitelisted tables are used
        tables_match = re.findall(r"\bFROM\s+(\w+)", cleaned, re.IGNORECASE)
        if tables_match:
            for table in tables_match:
                if table.lower() not in ALLOWED_TABLES:
                    logger.warning(
                        f"SQL validation failed: table {table} not in whitelist in: {sql}"
                    )
                    return False

        return True

    async def execute_sql(self, sql: str) -> list[dict[str, object]]:
        """Выполнить SQL запрос (read-only)."""
        if not self.validate_sql(sql):
            raise ValueError(f"Invalid SQL query: {sql}")

        session_gen = self.session_factory()
        session = await session_gen.__anext__()

        try:
            result = await session.execute(text(sql))
            rows = result.fetchall()

            # Convert rows to list of dicts
            if rows:
                # Get column names from result
                columns = result.keys()
                return [dict(zip(columns, row, strict=False)) for row in rows]
            return []

        except Exception as e:
            logger.error(f"SQL execution error: {e}")
            raise

        finally:
            await session_gen.aclose()

    async def process_query(self, user_query: str) -> Text2SQLResponse:
        """
        Обработать Text2SQL запрос.

        1. Отправить вопрос в LLM с Text2SQL промптом
        2. Извлечь SQL из ответа
        3. Валидировать SQL (только SELECT, whitelist таблиц)
        4. Выполнить SQL (read-only)
        5. Отправить результаты обратно в LLM
        6. Получить финальный ответ
        """
        try:
            # Validate empty query
            if not user_query or not user_query.strip():
                raise ValueError("Query cannot be empty")

            # Step 1: Send question to LLM for SQL generation
            logger.debug(f"Processing Text2SQL query: {user_query}")

            # Create message for LLM
            history = [
                ChatMessage(role="system", content=self.text2sql_prompt),
                ChatMessage(role="user", content=user_query),
            ]

            # Get SQL from LLM
            llm_response = await self.llm_client.get_response(history)
            logger.debug(f"LLM response: {llm_response}")

            # Extract SQL from response
            # Try to find SQL query in response (wrapped in markers or code blocks)
            sql_match = re.search(
                r"```(?:sql)?\s*\n(.*?)\n```", llm_response, re.DOTALL | re.IGNORECASE
            )
            sql_query = sql_match.group(1).strip() if sql_match else llm_response.strip()

            # Clean up SQL - remove any remaining markdown artifacts
            sql_query = re.sub(r"```\s*(?:sql)?\s*", "", sql_query).strip()

            # Validate SQL
            if not self.validate_sql(sql_query):
                raise ValueError(f"Invalid or unsafe SQL query: {sql_query}")

            # Execute SQL
            result = await self.execute_sql(sql_query)

            # Return response with SQL, result, and interpretation
            return Text2SQLResponse(
                sql=sql_query,
                result=result,
                interpretation=f"Query returned {len(result)} row(s)",
            )

        except Exception as e:
            logger.error(f"Error processing Text2SQL query: {e}")
            raise
