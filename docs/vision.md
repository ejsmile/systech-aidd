# Техническое видение проекта

## 1. Технологии

### Основной стек
- **Python 3.11+** - язык программирования
- **uv** - управление зависимостями и виртуальным окружением
- **aiogram 3.x** - асинхронный фреймворк для Telegram Bot API (метод polling)
- **openai** - клиент для работы с LLM через провайдер OpenRouter
- **make** - автоматизация задач сборки и запуска

### Дополнительные библиотеки
- **pydantic** - валидация данных
- **pydantic-settings** - загрузка и валидация конфигурации из переменных окружения
- **python-dotenv** - работа с .env файлами
- **dataclasses** (стандартная библиотека Python) - классы данных
- **logging** (стандартная библиотека Python) - логирование

### Хранение данных
- История диалогов хранится в оперативной памяти (без персистентности)

## 2. Принцип разработки

### Основные принципы
1. **KISS (Keep It Simple, Stupid)** - максимальная простота решения
2. **ООП с правилом: 1 класс = 1 файл** - четкая структура, легкая навигация
3. **Асинхронность** - использование async/await (требование aiogram)
4. **Конфигурация через переменные окружения** - гибкость без изменения кода
5. **Раннее обнаружение ошибок** - валидация конфигурации при старте
6. **Graceful degradation** - корректная обработка ошибок, бот продолжает работать даже при недоступности LLM

### Чего НЕ делаем (избегаем оверинжиниринга)
- ❌ Сложные паттерны проектирования
- ❌ Абстракции "на будущее"
- ❌ Микросервисная архитектура
- ❌ Сложные DI-контейнеры
- ❌ Избыточное тестирование на старте

## 3. Структура проекта

```
systech-aidd-my/
├── src/                    # Исходный код
│   ├── __init__.py
│   ├── main.py            # Точка входа в приложение
│   ├── bot.py             # Класс Bot - инициализация aiogram
│   ├── handlers.py        # Класс MessageHandler - обработка сообщений
│   ├── llm_client.py      # Класс LLMClient - работа с OpenRouter
│   ├── conversation.py    # Класс ConversationManager - управление историей
│   ├── models.py          # Классы данных: ConversationKey, Message
│   └── config.py          # Класс Config - конфигурация
├── docs/                  # Документация
│   ├── idea.md
│   └── vision.md
├── .env.example           # Пример конфигурации
├── .gitignore
├── Makefile              # Команды для сборки и запуска
├── pyproject.toml        # Конфигурация проекта и зависимостей
├── uv.lock               # Lockfile с точными версиями зависимостей
└── README.md
```

### Описание ключевых файлов
- **main.py** - запуск бота, связывание компонентов
- **bot.py** - создание и настройка aiogram Bot и Dispatcher
- **handlers.py** - обработка входящих сообщений из Telegram
- **llm_client.py** - отправка запросов к LLM через OpenRouter
- **conversation.py** - хранение истории диалога в памяти
- **models.py** - классы данных (ConversationKey, Message)
- **config.py** - загрузка и валидация конфигурации
- **pyproject.toml** - метаданные проекта и список зависимостей
- **uv.lock** - lockfile с точными версиями всех зависимостей (создаётся автоматически)

### Пример pyproject.toml

```toml
[project]
name = "systech-aidd-my"
version = "0.1.0"
description = "LLM-ассистент в виде Telegram-бота"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "aiogram>=3.0.0",
    "openai>=1.0.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "python-dotenv>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

## 4. Архитектура проекта

### Схема взаимодействия компонентов
```
Telegram User
      ↓
   [aiogram Bot] (bot.py)
      ↓
[MessageHandler] (handlers.py)
      ↓
[ConversationManager] (conversation.py) ←→ [LLMClient] (llm_client.py)
      ↓                                            ↓
История в памяти                          OpenRouter API
```

### Поток обработки сообщения
1. **Пользователь** отправляет сообщение в Telegram
2. **Bot** (aiogram) получает сообщение через polling
3. **MessageHandler** обрабатывает входящее сообщение
4. **ConversationManager** добавляет сообщение в историю диалога
5. **LLMClient** отправляет историю + системный промпт в OpenRouter
6. **OpenRouter** возвращает ответ от LLM
7. **ConversationManager** добавляет ответ в историю
8. **MessageHandler** отправляет ответ пользователю через Bot

### Ответственности классов
- **Config** - хранит конфигурацию (токены, URL, параметры LLM)
- **Bot** - обертка над aiogram Bot + Dispatcher, регистрация handlers
- **MessageHandler** - обработка команд и текстовых сообщений
- **ConversationManager** - управление историей диалогов (dict: ConversationKey → list[Message])
- **LLMClient** - асинхронные запросы к OpenRouter API
- **ConversationKey** - immutable ключ для идентификации диалога (chat_id + user_id)
- **Message** - структура сообщения (role + content)

## 5. Модель данных

### Конфигурация (Config)
```python
telegram_token: str          # Токен Telegram бота
openrouter_api_key: str      # API ключ OpenRouter
openrouter_base_url: str     # URL OpenRouter (по умолчанию: "https://openrouter.ai/api/v1")
model_name: str              # Название модели (например: "anthropic/claude-3.5-sonnet")
system_prompt: str           # Системный промпт для роли бота
max_history_messages: int    # Максимум сообщений в истории (по умолчанию: 20)
temperature: float           # Температура генерации LLM (по умолчанию: 0.7)
log_level: str               # Уровень логирования (по умолчанию: "INFO")
```

### История диалога (ConversationManager)
```python
# Классы данных:
@dataclass(frozen=True)  # frozen=True для использования как ключ словаря
class ConversationKey:
    chat_id: int
    user_id: int

@dataclass
class Message:
    role: str      # "system", "user", или "assistant"
    content: str

# Структура в памяти:
conversations: dict[ConversationKey, list[Message]]

# Ключ: ConversationKey(chat_id, user_id) - для учета переподключений
# Значение: список сообщений в формате OpenAI API
# Ограничение: последние 20 сообщений (+ system prompt)
```

### Встроенные типы
- **Telegram Message** - используем типы aiogram (Message)
- **LLM Request/Response** - используем формат OpenAI API (совместимый с OpenRouter)

## 6. Работа с LLM

### Реализация (LLMClient)
- Библиотека: `openai` с настройкой `base_url` на OpenRouter
- Асинхронные запросы: `async/await`
- Метод: `client.chat.completions.create()`
- Формат: OpenAI Chat Completions API
- Таймаут: 30 секунд (настройка клиента при инициализации)

### Параметры запроса
```python
{
  "model": model_name,              # Из конфигурации
  "messages": conversation_history,  # Из ConversationManager
  "temperature": temperature,        # Из конфигурации
  "stream": False                   # Без стриминга для простоты
}
```

### Обработка ошибок
Простой подход без retry:
- Любая ошибка (Timeout, API Error, Rate Limit, etc.) → логируем детали
- Пользователю отправляем простое сообщение: "Произошла ошибка при обработке запроса. Попробуйте позже."

## 7. Сценарии работы

### Сценарий 1: Начало работы (`/start`)
1. Пользователь отправляет команду `/start`
2. Бот отвечает приветственным сообщением
3. Для этого пользователя создается новая пустая история диалога

### Сценарий 2: Обычное сообщение
1. Пользователь отправляет текстовое сообщение
2. Бот добавляет сообщение в историю
3. Бот отправляет историю в LLM
4. Бот получает ответ и добавляет его в историю
5. Бот отправляет ответ пользователю

### Сценарий 3: Очистка истории (`/clear`)
1. Пользователь отправляет команду `/clear`
2. Бот очищает историю диалога для этого пользователя
3. Бот подтверждает: "История диалога очищена"

### Сценарий 4: Справка (`/help`)
1. Пользователь отправляет команду `/help`
2. Бот отправляет список доступных команд:
   - `/start` - начать работу
   - `/clear` - очистить историю диалога
   - `/help` - показать справку

### Обработка других типов сообщений
- Фото, видео, стикеры, файлы и другие типы сообщений игнорируются
- При ошибках бот отправляет сообщение об ошибке и продолжает работать

## 8. Подход к конфигурированию

### Источник конфигурации
- Все настройки через **переменные окружения**
- Файл `.env` для локальной разработки (не в git)
- Файл `.env.example` с примером конфигурации (в git)

### Переменные окружения
```bash
# Обязательные
TELEGRAM_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key

# Необязательные (с значениями по умолчанию)
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT="Ты полезный ассистент."
MAX_HISTORY_MESSAGES=20
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

### Валидация конфигурации
- Загрузка через `pydantic_settings.BaseSettings` (Pydantic v2)
- Валидация при старте приложения (fail-fast принцип)
- Если обязательные переменные не заданы → приложение не запускается с понятным сообщением об ошибке

### Использование в коде
```python
config = Config()  # Автоматически загружает из .env
llm_client = LLMClient(config)
bot = Bot(config)
```

## 9. Подход к логгированию

### Библиотека
- Стандартный модуль Python `logging` (без дополнительных зависимостей)

### Уровни логирования
- **DEBUG** - все сообщения пользователей и ответы LLM (только для отладки)
- **INFO** - старт/стоп бота, обработка команд
- **WARNING** - необычные ситуации (неподдерживаемые типы сообщений)
- **ERROR** - ошибки при работе с LLM API, сетевые ошибки

### Конфигурация
```bash
# Добавляем в переменные окружения
LOG_LEVEL=DEBUG  # DEBUG для разработки, INFO для продакшена
```

### Формат логов
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Настройка
- Вывод в консоль (stdout)
- Уровень задается через переменную окружения `LOG_LEVEL` (по умолчанию: `INFO`)
- Настройка один раз в `main.py` при старте

### Что логируем
**DEBUG режим (для разработки):**
- ✅ Все сообщения от пользователей (содержимое)
- ✅ Все ответы от LLM (содержимое)
- ✅ Детали запросов к API

**INFO режим и выше (для продакшена):**
- ✅ Старт/остановка бота
- ✅ Получение команд от пользователей (без содержимого)
- ✅ Ошибки при запросах к LLM (с текстом ошибки)
- ✅ Ошибки валидации конфигурации
- ❌ Содержимое сообщений пользователей (приватность)
- ❌ Ответы от LLM (приватность)

### Пример использования
```python
logger = logging.getLogger(__name__)
logger.info("Bot started successfully")
logger.debug(f"User message: {message.text}")
logger.debug(f"LLM response: {response}")
logger.error(f"LLM API error: {error}")
```

## 10. Локальная разработка

### Требования к окружению
- **Python 3.11+** - установленный интерпретатор Python
- **uv** - менеджер пакетов и виртуальных окружений
- **make** - для автоматизации команд (опционально)
- **Telegram Bot Token** - получить через [@BotFather](https://t.me/botfather)
- **OpenRouter API Key** - получить на [openrouter.ai](https://openrouter.ai)

### Установка и запуск
1. Создать виртуальное окружение: `uv venv`
2. Установить зависимости: `uv pip install -e .` или `make install`
3. Настроить `.env` файл (обязательные: `TELEGRAM_TOKEN`, `OPENROUTER_API_KEY`)
4. Запустить: `python src/main.py` или `make run`

### Команды Makefile
- `make install` - установить зависимости
- `make run` - запустить бота
- `make dev` - запустить в режиме разработки (LOG_LEVEL=DEBUG)
- `make lint` - проверить код линтером
- `make format` - форматировать код
- `make clean` - очистить временные файлы

### Режим отладки
Для детального логирования установить `LOG_LEVEL=DEBUG` в `.env` или через переменную окружения.

⚠️ **Важно:** DEBUG режим логирует содержимое сообщений - не используйте в продакшене!

---

## Итого

Документ технического видения проекта завершен. Все разделы описывают минимальное простое решение для проверки идеи согласно принципам KISS и ООП.

