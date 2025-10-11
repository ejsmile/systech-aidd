import logging

from openai import AsyncOpenAI

from .config import Config
from .models import ChatMessage

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(self, config: Config) -> None:
        self.config: Config = config
        self.client: AsyncOpenAI = AsyncOpenAI(
            api_key=config.openrouter_api_key,
            base_url=config.openrouter_base_url,
            timeout=30.0,
        )

    async def get_response(self, messages: list[ChatMessage]) -> str:
        """
        Получить ответ от LLM

        Args:
            messages: История диалога (список ChatMessage)

        Returns:
            Текст ответа от LLM

        Raises:
            Exception: При ошибке запроса к API
        """
        try:
            logger.debug(f"Sending {len(messages)} messages to LLM")

            # Конвертация в формат OpenAI API
            api_messages = [msg.to_dict() for msg in messages]

            # Запрос к LLM
            response = await self.client.chat.completions.create(
                model=self.config.model_name,
                messages=api_messages,  # type: ignore[arg-type]
                temperature=self.config.temperature,
            )

            # Извлечение текста ответа
            answer = response.choices[0].message.content
            if answer is None:
                raise ValueError("LLM returned empty response")
            logger.debug(f"LLM response: {answer}")

            return answer

        except Exception as e:
            logger.error(f"LLM API error: {e}")
            raise
