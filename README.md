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
# База данных
make db-up         # Запустить PostgreSQL в Docker
make db-down       # Остановить PostgreSQL
make db-migrate    # Применить миграции
make db-reset      # Сбросить и пересоздать БД

# Запуск
make run           # Запустить бота
make dev           # Запустить в DEBUG режиме
make restart       # Перезапустить бота

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
│   ├── main.py           # Точка входа
│   ├── bot.py            # Bot - aiogram wrapper
│   ├── handlers.py       # MessageHandler - обработка сообщений
│   ├── llm_client.py     # LLMClient - работа с OpenRouter
│   ├── conversation.py   # ConversationManager - история диалогов
│   ├── repository.py     # MessageRepository - работа с БД
│   ├── database.py       # Database - управление подключением
│   ├── db_models.py      # SQLAlchemy модели
│   ├── models.py         # Модели данных
│   └── config.py         # Config - конфигурация
├── alembic/              # Миграции базы данных
├── tests/                # Автоматизированные тесты (51 тест, coverage 84%)
├── docs/                 # Документация
├── docker-compose.yml    # PostgreSQL для разработки
├── Makefile             # Команды разработки
└── pyproject.toml       # Конфигурация проекта
```

Детальное описание архитектуры см. в [docs/vision.md](docs/vision.md)

## 🛠 Технологии

- **Python 3.11+** с async/await
- **aiogram 3.x** - Telegram Bot API
- **OpenRouter** - доступ к LLM моделям
- **PostgreSQL 16** - персистентное хранение истории
- **SQLAlchemy 2.x (async)** - ORM для работы с БД
- **Alembic** - миграции базы данных
- **Docker Compose** - локальная инфраструктура
- **uv** - управление зависимостями
- **ruff + mypy + pytest** - качество кода
- **testcontainers** - изолированные тесты

Полный стек см. в [docs/vision.md](docs/vision.md)

## 💡 Принципы разработки

- **KISS** - максимальная простота решений
- **1 класс = 1 файл** - четкая структура
- **Type hints везде** - mypy strict mode
- **Async/await** - асинхронность по умолчанию
- **Coverage >80%** - качественное тестирование (текущий: 84%, 51 тест)
- **Testcontainers** - изолированные тесты с реальной БД

Подробные правила см. в [.cursor/rules/conventions.mdc](.cursor/rules/conventions.mdc)

## ✅ Контроль качества

```bash
make quality    # format + lint + typecheck
make test-cov   # тесты с coverage отчетом
```

Workflow разработки см. в [.cursor/rules/workflow.mdc](.cursor/rules/workflow.mdc)

## 📚 Документация

- **[docs/idea.md](docs/idea.md)** - концепция проекта
- **[docs/vision.md](docs/vision.md)** - техническое видение и архитектура
- **[docs/roadmap.md](docs/roadmap.md)** - роадмап и спринты проекта
- **[.cursor/rules/conventions.mdc](.cursor/rules/conventions.mdc)** - правила разработки
- **[.cursor/rules/workflow.mdc](.cursor/rules/workflow.mdc)** - workflow разработки

## 🎯 Команды бота

- `/start` - начать работу с ботом
- `/help` - показать справку по командам
- `/clear` - очистить историю диалога (soft delete)
- `/role` - показать текущую роль ассистента

## 📝 Лицензия

См. [LICENSE](LICENSE)
