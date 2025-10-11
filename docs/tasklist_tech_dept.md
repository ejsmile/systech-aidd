# 📋 План технического долга systech-aidd

> **Базовые документы:** @tasklist.md, @vision.md, @conventions.mdc, @workflow.mdc

## 📊 Отчет о прогрессе

| № | Итерация | Статус | Проверка качества | Дата завершения |
|---|----------|--------|-------------------|-----------------|
| 1 | Инструменты качества кода | ✅ Завершено | format: ✅, lint: ✅, typecheck: ✅ | 2025-10-11 |
| 2 | Рефакторинг моделей данных | ✅ Завершено | format: ✅, lint: ✅, typecheck: ✅, imports: ✅ | 2025-10-11 |
| 3 | Структура тестирования | ✅ Завершено | tests: ✅ (4 passed), coverage: 22% (models: 100%) | 2025-10-11 |
| 4 | Базовые unit-тесты | ✅ Завершено | tests: ✅ (12 passed), coverage: 49% (conversation: 94%, llm: 100%) | 2025-10-11 |
| 5 | Покрытие интеграционными тестами | ⏳ Ожидает | - | - |

**Легенда статусов:**
- ⏳ Ожидает
- 🔄 В работе
- ✅ Завершено
- ⚠️ Проблемы

---

## 🛠️ Итерация 1: Инструменты качества кода

**Цель:** Настроить автоматизированные инструменты контроля качества (форматтер, линтер, type checker)

### Задачи
- [x] Добавить `ruff` в dev-зависимости pyproject.toml
- [x] Добавить `mypy` в dev-зависимости pyproject.toml
- [x] Настроить `[tool.ruff]` в pyproject.toml
- [x] Настроить `[tool.mypy]` в pyproject.toml
- [x] Добавить команды в Makefile: `format`, `lint`, `typecheck`, `quality`
- [x] Запустить `ruff format .` на всем коде
- [x] Запустить `ruff check . --fix` и исправить ошибки
- [x] Добавить type hints для всех классов и функций
- [x] Запустить `mypy src/` и исправить type hints

### Конфигурация

**pyproject.toml:**
```toml
[project.optional-dependencies]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
]

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C90", "PL"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Makefile команды:**
```makefile
format:
	uv run ruff format .

lint:
	uv run ruff check . --fix

typecheck:
	uv run mypy src/

quality: format lint typecheck
	@echo "✅ Code quality checks passed"
```

**Примеры добавления type hints:**
```python
# Классы
class ConversationManager:
    def __init__(self, max_history_messages: int = 20) -> None:
        self.conversations: dict[ConversationKey, list[ChatMessage]] = {}
        self.max_history_messages: int = max_history_messages
    
    def add_message(self, key: ConversationKey, message: ChatMessage) -> None:
        """Добавляет сообщение в историю диалога"""
        ...
    
    def get_history(
        self, 
        key: ConversationKey, 
        system_prompt: str
    ) -> list[ChatMessage]:
        """Возвращает историю диалога с system prompt"""
        ...

# Функции
async def handle_message(message: Message, bot: Bot) -> None:
    """Обработчик текстовых сообщений"""
    ...

# Async функции
async def get_response(self, messages: list[ChatMessage]) -> str:
    """Получает ответ от LLM"""
    ...
```

### Проверка соответствия
- [x] ✅ Код следует KISS принципу (@conventions.mdc)
- [x] ✅ Следование правилам 1 класс = 1 файл (@conventions.mdc)
- [x] ✅ Все async/await на месте (@conventions.mdc)
- [x] ✅ Правильная структура импортов (@conventions.mdc)
- [x] ✅ Type hints для всех классов, методов и функций (@conventions.mdc)
- [x] ✅ Логирование соответствует уровням (@vision.md, раздел 9)
- [x] ✅ Согласование перед реализацией (@workflow.mdc)

### Тест
```bash
# Установить dev-зависимости
make install-dev  # или: uv pip install -e ".[dev]"

# Запустить проверки качества
make quality

# Должны пройти:
# 1. ruff format - код отформатирован
# 2. ruff check - нет ошибок линтера
# 3. mypy - нет type errors, все функции и классы имеют type hints

# Проверить type hints отдельно
make typecheck
# Должен пройти без ошибок:
# - все функции имеют аннотации параметров и return type
# - все методы классов имеют аннотации
# - все атрибуты классов имеют type hints

# Проверить tasks.json в Cursor
# Tasks -> Run Task -> выбрать любую задачу (Format, Lint, Type Check)
```

---

## 🔄 Итерация 2: Рефакторинг моделей данных

**Цель:** Устранить конфликт имен Message, добавить валидацию ролей, улучшить type safety

### Задачи
- [x] Переименовать `Message` → `ChatMessage` в `models.py`
- [x] Добавить `Role` enum для валидации ролей
- [x] Использовать `Literal` type hint для role
- [x] Обновить все импорты в `handlers.py`
- [x] Обновить все импорты в `llm_client.py`
- [x] Обновить все импорты в `conversation.py`
- [x] Убрать workaround `from .models import Message as LLMMessage`
- [x] Добавить docstrings для ChatMessage и ConversationKey
- [x] Запустить `make quality` для проверки

### Реализация

**src/models.py:**
```python
from dataclasses import dataclass
from enum import Enum
from typing import Literal


class Role(str, Enum):
    """Роли участников диалога"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True)
class ConversationKey:
    """
    Immutable ключ для идентификации диалога.
    
    Комбинация chat_id + user_id позволяет различать пользователей
    в групповых чатах и приватных диалогах.
    """
    chat_id: int
    user_id: int


@dataclass
class ChatMessage:
    """
    Сообщение в диалоге с LLM.
    
    Формат совместим с OpenAI Chat Completions API.
    """
    role: Literal["system", "user", "assistant"]
    content: str
    
    def to_dict(self) -> dict[str, str]:
        """Конвертация в формат OpenAI API"""
        return {"role": self.role, "content": self.content}
```

### Проверка соответствия
- [x] ✅ Нет конфликта имен с aiogram.types.Message
- [x] ✅ Валидация роли через Literal (@conventions.mdc)
- [x] ✅ Docstrings для неочевидной логики (@conventions.mdc)
- [x] ✅ Код следует KISS принципу (@conventions.mdc)
- [x] ✅ Правильное использование dataclass (@conventions.mdc)
- [x] ✅ Type hints везде (@conventions.mdc + mypy)
- [x] ✅ Согласование перед реализацией (@workflow.mdc)

### Тест
```bash
# Запустить бота
make run

# В Telegram:
/start
"Привет!"  → Должен работать как раньше
"Как дела?" → Должен работать как раньше
/clear

# Проверить качество кода
make quality

# Проверить отсутствие ошибок импорта
uv run python -c "from src.models import ChatMessage, Role, ConversationKey; print('OK')"
```

---

## 🧪 Итерация 3: Структура тестирования

**Цель:** Создать структуру для автоматизированного тестирования

### Задачи
- [x] Создать директорию `tests/`
- [x] Создать `tests/__init__.py`
- [x] Создать `tests/conftest.py` с общими fixtures
- [x] Добавить `pytest` и `pytest-asyncio` в dev-зависимости (уже есть)
- [x] Добавить `pytest-cov` для coverage (уже есть)
- [x] Настроить `[tool.pytest.ini_options]` в pyproject.toml
- [x] Добавить команды в Makefile: `test`, `test-cov`
- [x] Создать `.coveragerc` для настройки coverage
- [x] Создать примеры тестов `tests/test_models.py`

### Реализация

**tests/conftest.py:**
```python
"""Общие fixtures для тестов"""
import pytest
from src.config import Config
from src.conversation import ConversationManager


@pytest.fixture
def mock_config():
    """Минимальная валидная конфигурация для тестов"""
    return Config(
        telegram_token="test_token_123",
        openrouter_api_key="test_api_key_123",
    )


@pytest.fixture
def conversation_manager():
    """ConversationManager с настройками для тестов"""
    return ConversationManager(max_history_messages=3)
```

**tests/test_models.py:**
```python
"""Тесты для моделей данных"""
from src.models import ChatMessage, ConversationKey, Role


def test_conversation_key_frozen():
    """ConversationKey должен быть immutable"""
    key = ConversationKey(chat_id=1, user_id=1)
    assert key.chat_id == 1
    assert key.user_id == 1
    
    # Должна быть ошибка при попытке изменить
    try:
        key.chat_id = 2
        assert False, "ConversationKey должен быть frozen"
    except AttributeError:
        pass


def test_conversation_key_hashable():
    """ConversationKey должен быть hashable для использования как ключ dict"""
    key1 = ConversationKey(chat_id=1, user_id=1)
    key2 = ConversationKey(chat_id=1, user_id=1)
    key3 = ConversationKey(chat_id=2, user_id=1)
    
    assert key1 == key2
    assert key1 != key3
    assert hash(key1) == hash(key2)


def test_chat_message_to_dict():
    """ChatMessage.to_dict() должен возвращать формат OpenAI API"""
    msg = ChatMessage(role="user", content="test")
    result = msg.to_dict()
    
    assert result == {"role": "user", "content": "test"}


def test_role_enum():
    """Role enum должен содержать правильные значения"""
    assert Role.SYSTEM == "system"
    assert Role.USER == "user"
    assert Role.ASSISTANT == "assistant"
```

**pyproject.toml дополнение:**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

**Makefile команды:**
```makefile
test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

test-watch:
	uv run pytest-watch tests/ -v
```

### Проверка соответствия
- [x] ✅ Структура тестов понятная и простая (@conventions.mdc - KISS)
- [x] ✅ Следование принципу 1 класс = 1 файл теста (@conventions.mdc)
- [x] ✅ Fixtures переиспользуемые (@conventions.mdc)
- [x] ✅ Тесты изолированные и быстрые
- [x] ✅ Минимум mock'ов на начальном этапе (@vision.md)
- [x] ✅ Согласование перед реализацией (@workflow.mdc)

### Тест
```bash
# Запустить тесты
make test

# Должны пройти все тесты test_models.py
# Expected: 4 passed in X.XXs

# Проверить coverage
make test-cov

# Должен показать coverage report
# Открыть htmlcov/index.html для детального отчета
```

---

## 🧪 Итерация 4: Базовые unit-тесты

**Цель:** Покрыть тестами критичные компоненты (ConversationManager, LLMClient mock)

### Задачи
- [x] Создать `tests/test_conversation.py`
- [x] Тесты для `add_message()`
- [x] Тесты для `get_history()` с system prompt
- [x] Тесты для `clear_history()`
- [x] Тесты для ограничения истории (max_history_messages)
- [x] Создать `tests/test_llm_client.py` с mock'ами
- [x] Тест для `get_response()` с mock OpenAI API
- [x] Тест для обработки ошибок LLM API
- [x] Запустить `make test-cov` и проверить coverage > 70%

### Реализация

**tests/test_conversation.py:**
```python
"""Тесты для ConversationManager"""
import pytest
from src.conversation import ConversationManager
from src.models import ConversationKey, ChatMessage


@pytest.fixture
def manager():
    return ConversationManager(max_history_messages=3)


def test_add_message(manager):
    """Добавление сообщения в историю"""
    key = ConversationKey(chat_id=1, user_id=1)
    msg = ChatMessage(role="user", content="test")
    
    manager.add_message(key, msg)
    
    assert key in manager.conversations
    assert len(manager.conversations[key]) == 1
    assert manager.conversations[key][0] == msg


def test_get_history_with_system_prompt(manager):
    """История должна включать system prompt"""
    key = ConversationKey(chat_id=1, user_id=1)
    system_prompt = "You are helpful assistant"
    
    history = manager.get_history(key, system_prompt)
    
    assert len(history) == 1
    assert history[0].role == "system"
    assert history[0].content == system_prompt


def test_history_limit(manager):
    """История должна ограничиваться max_history_messages"""
    key = ConversationKey(chat_id=1, user_id=1)
    system_prompt = "test"
    
    # Добавляем 5 сообщений (limit = 3)
    for i in range(5):
        manager.add_message(key, ChatMessage(role="user", content=f"msg{i}"))
    
    history = manager.get_history(key, system_prompt)
    
    # system + 3 последних сообщения
    assert len(history) == 4
    assert history[0].role == "system"
    assert history[-1].content == "msg4"  # последнее
    assert history[1].content == "msg2"  # 3-е с конца


def test_clear_history(manager):
    """Очистка истории диалога"""
    key = ConversationKey(chat_id=1, user_id=1)
    manager.add_message(key, ChatMessage(role="user", content="test"))
    
    assert key in manager.conversations
    
    manager.clear_history(key)
    
    assert key not in manager.conversations


def test_multiple_conversations(manager):
    """Разные пользователи имеют разные истории"""
    key1 = ConversationKey(chat_id=1, user_id=1)
    key2 = ConversationKey(chat_id=1, user_id=2)
    
    manager.add_message(key1, ChatMessage(role="user", content="user1"))
    manager.add_message(key2, ChatMessage(role="user", content="user2"))
    
    assert len(manager.conversations[key1]) == 1
    assert len(manager.conversations[key2]) == 1
    assert manager.conversations[key1][0].content == "user1"
    assert manager.conversations[key2][0].content == "user2"
```

**tests/test_llm_client.py:**
```python
"""Тесты для LLMClient"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.llm_client import LLMClient
from src.models import ChatMessage


@pytest.fixture
def mock_config():
    from src.config import Config
    return Config(
        telegram_token="test",
        openrouter_api_key="test",
    )


@pytest.mark.asyncio
async def test_get_response_success(mock_config):
    """Успешный запрос к LLM API"""
    client = LLMClient(mock_config)
    
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "test response"
    
    with patch.object(client.client.chat.completions, 'create', 
                     new=AsyncMock(return_value=mock_response)):
        messages = [ChatMessage(role="user", content="test")]
        response = await client.get_response(messages)
        
        assert response == "test response"


@pytest.mark.asyncio
async def test_get_response_api_error(mock_config):
    """Обработка ошибки LLM API"""
    client = LLMClient(mock_config)
    
    with patch.object(client.client.chat.completions, 'create',
                     new=AsyncMock(side_effect=Exception("API Error"))):
        messages = [ChatMessage(role="user", content="test")]
        
        with pytest.raises(Exception) as exc_info:
            await client.get_response(messages)
        
        assert "API Error" in str(exc_info.value)
```

### Проверка соответствия
- [x] ✅ Тесты изолированные и быстрые (@conventions.mdc)
- [x] ✅ Понятные названия тестов (@conventions.mdc)
- [x] ✅ Минимум mock'ов, только где необходимо (@vision.md)
- [x] ✅ Coverage критичных компонентов > 70% (conversation: 94%, llm: 100%)
- [x] ✅ Все тесты проходят (12 passed in 0.63s)
- [x] ✅ Согласование перед реализацией (@workflow.mdc)

### Тест
```bash
# Запустить все тесты
make test

# Проверить coverage
make test-cov

# Должны пройти:
# test_conversation.py - 5 tests
# test_llm_client.py - 2 tests
# test_models.py - 4 tests
# Total: 11 tests passed

# Coverage должен быть > 70% для src/conversation.py и src/models.py
```

---

## 🚀 Итерация 5: Покрытие интеграционными тестами

**Цель:** Добавить интеграционные тесты для критичных сценариев

### Задачи
- [ ] Создать `tests/test_integration.py`
- [ ] Тест полного цикла: user message → LLM → response
- [ ] Тест истории диалога с контекстом
- [ ] Тест очистки истории и потери контекста
- [ ] Тест ограничения истории
- [ ] Создать `tests/test_config.py` для валидации конфигурации
- [ ] Обновить CI/CD готовность (документация для GitHub Actions)
- [ ] Запустить `make quality && make test-cov` - все проходит

### Реализация

**tests/test_integration.py:**
```python
"""Интеграционные тесты для полного цикла работы"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.conversation import ConversationManager
from src.llm_client import LLMClient
from src.models import ConversationKey, ChatMessage
from src.config import Config


@pytest.fixture
def config():
    return Config(
        telegram_token="test",
        openrouter_api_key="test",
        system_prompt="You are helpful assistant",
        max_history_messages=3,
    )


@pytest.fixture
def manager(config):
    return ConversationManager(max_history_messages=config.max_history_messages)


@pytest.fixture
def llm_client(config):
    return LLMClient(config)


@pytest.mark.asyncio
async def test_full_conversation_cycle(config, manager, llm_client):
    """Полный цикл: user message → LLM → response → history"""
    key = ConversationKey(chat_id=1, user_id=1)
    
    # Mock LLM response
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello! How can I help you?"
    
    with patch.object(llm_client.client.chat.completions, 'create',
                     new=AsyncMock(return_value=mock_response)):
        # User sends message
        user_msg = ChatMessage(role="user", content="Hello")
        manager.add_message(key, user_msg)
        
        # Get history with system prompt
        history = manager.get_history(key, config.system_prompt)
        
        # LLM processes
        response = await llm_client.get_response(history)
        
        # Add assistant response to history
        assistant_msg = ChatMessage(role="assistant", content=response)
        manager.add_message(key, assistant_msg)
        
        # Check final history
        final_history = manager.get_history(key, config.system_prompt)
        
        assert len(final_history) == 3  # system + user + assistant
        assert final_history[0].role == "system"
        assert final_history[1].content == "Hello"
        assert final_history[2].content == "Hello! How can I help you?"


@pytest.mark.asyncio
async def test_conversation_with_context(config, manager, llm_client):
    """LLM должен получать контекст предыдущих сообщений"""
    key = ConversationKey(chat_id=1, user_id=1)
    
    # Add previous messages
    manager.add_message(key, ChatMessage(role="user", content="My name is Pavel"))
    manager.add_message(key, ChatMessage(role="assistant", content="Nice to meet you, Pavel!"))
    
    # New message
    manager.add_message(key, ChatMessage(role="user", content="What is my name?"))
    
    history = manager.get_history(key, config.system_prompt)
    
    # Should contain all previous messages
    assert len(history) == 4  # system + 3 messages
    assert any("Pavel" in msg.content for msg in history)


def test_clear_context(config, manager):
    """После clear история должна быть пустой"""
    key = ConversationKey(chat_id=1, user_id=1)
    
    # Add messages
    manager.add_message(key, ChatMessage(role="user", content="Test 1"))
    manager.add_message(key, ChatMessage(role="assistant", content="Response 1"))
    
    # Clear
    manager.clear_history(key)
    
    # New history should only have system prompt
    history = manager.get_history(key, config.system_prompt)
    assert len(history) == 1
    assert history[0].role == "system"
```

**tests/test_config.py:**
```python
"""Тесты для валидации конфигурации"""
import pytest
from pydantic import ValidationError
from src.config import Config


def test_config_with_required_fields():
    """Конфигурация с обязательными полями"""
    config = Config(
        telegram_token="test_token",
        openrouter_api_key="test_key",
    )
    
    assert config.telegram_token == "test_token"
    assert config.openrouter_api_key == "test_key"
    assert config.model_name == "anthropic/claude-3.5-sonnet"  # default
    assert config.max_history_messages == 20  # default


def test_config_with_custom_values():
    """Конфигурация с кастомными значениями"""
    config = Config(
        telegram_token="test",
        openrouter_api_key="test",
        model_name="gpt-4",
        temperature=0.5,
        max_history_messages=10,
    )
    
    assert config.model_name == "gpt-4"
    assert config.temperature == 0.5
    assert config.max_history_messages == 10


def test_config_missing_required_field():
    """Ошибка при отсутствии обязательного поля"""
    with pytest.raises(ValidationError):
        Config(telegram_token="test")  # missing openrouter_api_key
```

### Проверка соответствия
- [ ] ✅ Интеграционные тесты покрывают критичные сценарии (@vision.md, раздел 7)
- [ ] ✅ Тесты конфигурации проверяют fail-fast (@vision.md, раздел 8)
- [ ] ✅ Все тесты проходят
- [ ] ✅ Coverage > 80% для критичных модулей
- [ ] ✅ `make quality` проходит без ошибок
- [ ] ✅ Согласование перед реализацией (@workflow.mdc)

### Тест
```bash
# Полная проверка качества
make quality

# Должно пройти: format, lint, typecheck

# Все тесты с coverage
make test-cov

# Должны пройти:
# test_models.py - 4 tests
# test_conversation.py - 5 tests
# test_llm_client.py - 2 tests
# test_config.py - 3 tests
# test_integration.py - 3 tests
# Total: 17 tests passed

# Coverage: > 80% для src/

# Проверить, что бот работает
make run
# В Telegram проверить все сценарии из @vision.md раздел 7
```

---

## 📝 Общие правила работы

### Перед каждой итерацией
1. ✅ Прочитать описание итерации
2. ✅ Проверить требования из @conventions.mdc и @vision.md
3. ✅ Согласовать план реализации (@workflow.mdc)
4. ✅ Дождаться подтверждения

### После каждой итерации
1. ✅ Выполнить все проверки соответствия
2. ✅ Запустить `make quality` - должно пройти
3. ✅ Запустить `make test` - все тесты проходят
4. ✅ Обновить таблицу прогресса
5. ✅ Сделать коммит: `feat: tech debt iteration X - [описание]`
6. ✅ Дождаться подтверждения перед следующей итерацией

### Приоритеты
- 🔥 **Критично:** Итерация 1 (инструменты), Итерация 2 (рефакторинг)
- ⚡ **Важно:** Итерация 3 (структура тестов), Итерация 4 (unit-тесты)
- 📈 **Желательно:** Итерация 5 (интеграционные тесты)

### Команды Make
```bash
make quality      # Полная проверка качества (format + lint + typecheck)
make test         # Запуск тестов
make test-cov     # Тесты с coverage
make run          # Запуск бота (для проверки работоспособности)
```

---

## 🎯 Цели технического долга

1. **Автоматизация контроля качества** - ruff, mypy
2. **Улучшение архитектуры** - устранение конфликтов, валидация
3. **Тестовое покрытие** - > 80% для критичных модулей
4. **Maintainability** - код легко поддерживать и развивать
5. **Соответствие vision.md** - следование всем принципам проекта


