# systech-aidd

LLM-ассистент в виде Telegram-бота для взаимодействия с пользователями через интеллектуальный диалог.

**Бот:** [@systtech_ai_bot_pk_bot](https://t.me/systtech_ai_bot_pk_bot)

## 🚀 Быстрый старт

### Требования
- **Python 3.11+** - требуемая версия
- **[uv](https://github.com/astral-sh/uv)** - менеджер пакетов и виртуальных окружений
- **Docker & Docker Compose** - для PostgreSQL
- **Telegram Bot Token** - получить у [@BotFather](https://t.me/botfather)
- **OpenRouter API Key** - получить на [openrouter.ai](https://openrouter.ai)

### Установка и запуск

```bash
# 1. Клонировать и перейти в директорию
git clone <repository-url>
cd systech-aidd-my

# 2. Установить зависимости
make install-dev    # включает dev-зависимости для тестирования

# 3. Настроить конфигурацию
cp sample.env .env
# Отредактировать .env и добавить токены

# 4. Запустить PostgreSQL
make db-up          # запускает PostgreSQL в Docker
make db-migrate     # применяет миграции

# 5. Запустить бота
make run        # или: make dev для DEBUG режима
```

### Конфигурация

Создайте файл `.env` в корне проекта:

```bash
# Обязательные
TELEGRAM_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key

# База данных
# Параметры (user, password, db, port) смотри в docker-compose.yml
DATABASE_URL=postgresql+asyncpg://aidd_user:aidd_password@localhost:5433/aidd_db

# Опциональные (значения по умолчанию)
MODEL_NAME=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT="Ты полезный ассистент."
SYSTEM_PROMPT_FILE=prompts/system.txt
MAX_HISTORY_MESSAGES=20
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

## 📋 Основные команды

```bash
# База данных (настройки в docker-compose.yml)
make db-up         # Запустить PostgreSQL в Docker
make db-down       # Остановить PostgreSQL
make db-migrate    # Применить миграции (автоматически при db-up)
make db-reset      # Сбросить и пересоздать БД

# Запуск
make run           # Запустить бота
make dev           # Запустить в DEBUG режиме
make restart       # Перезапустить бота

# API для веб-интерфейса
make run-api       # Запустить API сервер (http://localhost:8000)
make test-api      # Запустить тесты API

# Качество кода
make quality       # Полная проверка: format + lint + typecheck
make test          # Запустить все тесты
make test-cov      # Тесты с отчетом покрытия

# Разработка
make install-dev   # Установить dev-зависимости
make clean         # Очистить временные файлы
```

Полный список команд см. в [Makefile](Makefile)

## 📁 Структура проекта

```
systech-aidd-my/
├── src/                   # Исходный код (1 класс = 1 файл)
│   ├── main.py           # Точка входа для Telegram бота
│   ├── bot.py            # Bot - aiogram wrapper
│   ├── handlers.py       # Обработка сообщений и команд
│   ├── llm_client.py     # LLMClient - работа с OpenRouter
│   ├── conversation.py   # ConversationManager - история диалогов
│   ├── repository.py     # MessageRepository - работа с сообщениями
│   ├── user_repository.py # UserRepository - работа с пользователями
│   ├── database.py       # Database - управление подключением
│   ├── db_models.py      # SQLAlchemy модели (Message, User)
│   ├── models.py         # Модели данных (ChatMessage, UserData)
│   ├── config.py         # Config - конфигурация
│   └── api/              # FastAPI веб-интерфейс
│       ├── main.py       # Точка входа для API сервера
│       ├── app.py        # FastAPI приложение
│       ├── models.py     # Pydantic модели для API
│       ├── stat_collector.py     # Protocol для статистики
│       └── mock_stat_collector.py # Mock реализация
├── alembic/              # Миграции базы данных
├── tests/                # Автоматизированные тесты (105 тестов, coverage >85%)
├── docs/                 # Документация
│   ├── api/              # API документация
│   └── frontend/         # Frontend требования
├── docker-compose.yml    # PostgreSQL для разработки (настройки подключения)
├── Dockerfile.migrations # Docker для автоматических миграций
├── Makefile             # Команды разработки
└── pyproject.toml       # Конфигурация проекта
```

Детальное описание архитектуры см. в [docs/vision.md](docs/vision.md)

## 🛠 Технологии

### Backend
- **Python 3.11+** с async/await
- **aiogram 3.x** - Telegram Bot API
- **FastAPI** - REST API для веб-интерфейса
- **OpenRouter** - доступ к LLM моделям
- **PostgreSQL 16** - персистентное хранение истории
- **SQLAlchemy 2.x (async)** - ORM для работы с БД
- **Alembic** - миграции базы данных

### Infrastructure
- **Docker Compose** - локальная инфраструктура
- **uv** - управление зависимостями
- **uvicorn** - ASGI сервер для FastAPI

### Quality & Testing
- **ruff** - линтинг и форматирование
- **mypy (strict mode)** - проверка типов
- **pytest + pytest-asyncio** - тестирование
- **testcontainers** - изолированные тесты с реальной БД
- **Coverage >85%** - 105 тестов

Полный стек см. в [docs/vision.md](docs/vision.md)

## 💡 Принципы разработки

- **KISS** - максимальная простота решений
- **1 класс = 1 файл** - четкая структура
- **Type hints везде** - mypy strict mode
- **Async/await** - асинхронность по умолчанию
- **Coverage >85%** - качественное тестирование (105 тестов, API coverage 93%)
- **Testcontainers** - изолированные тесты с реальной БД

Подробные правила см. в [.cursor/rules/conventions.mdc](.cursor/rules/conventions.mdc)

## ✅ Контроль качества

```bash
make quality    # format + lint + typecheck
make test-cov   # тесты с coverage отчетом
```

Workflow разработки см. в [.cursor/rules/workflow.mdc](.cursor/rules/workflow.mdc)

## 📚 Документация

### Основная
- **[docs/idea.md](docs/idea.md)** - концепция проекта
- **[docs/vision.md](docs/vision.md)** - техническое видение и архитектура
- **[docs/roadmap.md](docs/roadmap.md)** - роадмап и спринты проекта
- **[docs/database_schema.md](docs/database_schema.md)** - схема базы данных (таблицы, индексы, связи)

### API для веб-интерфейса
- **[docs/api/api-contract.md](docs/api/api-contract.md)** - API контракт и endpoints
- **[docs/frontend/dashboard-requirements.md](docs/frontend/dashboard-requirements.md)** - требования к дашборду
- **http://localhost:8000/docs** - интерактивная OpenAPI документация (после `make run-api`)

### Разработка
- **[docker-compose.yml](docker-compose.yml)** - настройки PostgreSQL (user, password, db, port)
- **[.cursor/rules/conventions.mdc](.cursor/rules/conventions.mdc)** - правила разработки
- **[.cursor/rules/workflow.mdc](.cursor/rules/workflow.mdc)** - workflow разработки

## 🎯 Команды бота

- `/start` - начать работу с ботом
- `/help` - показать справку по командам
- `/clear` - очистить историю диалога (soft delete)
- `/role` - показать текущую роль ассистента

## 📝 Лицензия

См. [LICENSE](LICENSE)
