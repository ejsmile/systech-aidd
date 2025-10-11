"""Тесты для LLMClient"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.config import Config
from src.llm_client import LLMClient
from src.models import ChatMessage


@pytest.fixture
def mock_config() -> Config:
    return Config(
        telegram_token="test",
        openrouter_api_key="test",
    )


@pytest.mark.asyncio
async def test_get_response_success(mock_config: Config) -> None:
    """Успешный запрос к LLM API"""
    client = LLMClient(mock_config)

    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "test response"

    with patch.object(
        client.client.chat.completions, "create", new=AsyncMock(return_value=mock_response)
    ):
        messages = [ChatMessage(role="user", content="test")]
        response = await client.get_response(messages)

        assert response == "test response"


@pytest.mark.asyncio
async def test_get_response_empty_content(mock_config: Config) -> None:
    """Обработка пустого ответа от LLM"""
    client = LLMClient(mock_config)

    mock_response = MagicMock()
    mock_response.choices[0].message.content = None

    with patch.object(
        client.client.chat.completions, "create", new=AsyncMock(return_value=mock_response)
    ):
        messages = [ChatMessage(role="user", content="test")]

        with pytest.raises(ValueError, match="LLM returned empty response"):
            await client.get_response(messages)


@pytest.mark.asyncio
async def test_get_response_api_error(mock_config: Config) -> None:
    """Обработка ошибки LLM API"""
    client = LLMClient(mock_config)

    with patch.object(
        client.client.chat.completions, "create", new=AsyncMock(side_effect=Exception("API Error"))
    ):
        messages = [ChatMessage(role="user", content="test")]

        with pytest.raises(Exception) as exc_info:
            await client.get_response(messages)

        assert "API Error" in str(exc_info.value)
