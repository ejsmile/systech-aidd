# systech-aidd

LLM-ассистент в виде Telegram-бота для взаимодействия с пользователями через интеллектуальный диалог.

**Бот:** [@systtech_ai_bot_pk_bot](https://t.me/systtech_ai_bot_pk_bot)

## 🚀 Быстрый старт

### Требования
- **Python 3.11+** - требуемая версия
- **[uv](https://github.com/astral-sh/uv)** - менеджер пакетов и виртуальных окружений
- **Telegram Bot Token** - получить у [@BotFather](https://t.me/botfather)
- **OpenRouter API Key** - получить на [openrouter.ai](https://openrouter.ai)

### Установка и запуск

```bash
# 1. Клонировать и перейти в директорию
git clone <repository-url>
cd systech-aidd-my

# 2. Установить зависимости
make install    # или: uv venv && source .venv/bin/activate && uv pip install -e .

# 3. Настроить конфигурацию
cp sample.env .env
# Отредактировать .env и добавить токены

# 4. Запустить бота
make run        # или: python src/main.py
```

### Конфигурация

Создайте файл `.env` в корне проекта:

```bash
# Обязательные
TELEGRAM_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key

# Опциональные (значения по умолчанию)
MODEL_NAME=anthropic/claude-3.5-sonnet
SYSTEM_PROMPT="Ты полезный ассистент."
MAX_HISTORY_MESSAGES=20
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

## 📋 Основные команды

```bash
# Запуск
make run           # Запустить бота
make dev           # Запустить в DEBUG режиме

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
│   ├── models.py         # Модели данных
│   └── config.py         # Config - конфигурация
├── tests/                # Автоматизированные тесты
├── docs/                 # Документация
├── Makefile             # Команды разработки
└── pyproject.toml       # Конфигурация проекта
```

Детальное описание архитектуры см. в [docs/vision.md](docs/vision.md)

## 🛠 Технологии

- **Python 3.11+** с async/await
- **aiogram 3.x** - Telegram Bot API
- **OpenRouter** - доступ к LLM моделям
- **uv** - управление зависимостями
- **ruff + mypy + pytest** - качество кода

Полный стек см. в [docs/vision.md](docs/vision.md)

## 💡 Принципы разработки

- **KISS** - максимальная простота решений
- **1 класс = 1 файл** - четкая структура
- **Type hints везде** - mypy strict mode
- **Async/await** - асинхронность по умолчанию
- **Coverage >70%** - качественное тестирование

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
- **[.cursor/rules/conventions.mdc](.cursor/rules/conventions.mdc)** - правила разработки
- **[.cursor/rules/workflow.mdc](.cursor/rules/workflow.mdc)** - workflow разработки

## 🎯 Команды бота

- `/start` - начать работу
- `/clear` - очистить историю
- `/help` - показать справку

## 📝 Лицензия

См. [LICENSE](LICENSE)
