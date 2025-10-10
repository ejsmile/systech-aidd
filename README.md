# systech-aidd

LLM-ассистент в виде Telegram-бота для взаимодействия с пользователями через интеллектуальный диалог.

**Бот:** [@systtech_ai_bot_pk_bot](https://t.me/systtech_ai_bot_pk_bot)

## 🚀 Быстрый старт

### Требования
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - менеджер пакетов и виртуальных окружений
- Telegram Bot Token (получить у [@BotFather](https://t.me/botfather))
- OpenRouter API Key (получить на [openrouter.ai](https://openrouter.ai))

### Установка и запуск

```bash
# 1. Установить uv (если еще не установлен)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# или для Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Клонировать репозиторий
git clone <repository-url>
cd systech-aidd-my

# 3. Создать виртуальное окружение и установить зависимости
uv venv
source .venv/bin/activate  # macOS/Linux
# или .venv\Scripts\activate для Windows
uv pip install -e .

# 4. Настроить конфигурацию
cp sample.env .env
# Отредактировать .env и добавить токены

# 5. Запустить бота
python src/main.py
```

**Быстрая установка через Makefile:**
```bash
make install    # Создаст окружение и установит зависимости
make run        # Запустит бота
```

### Основные команды

```bash
make install    # Установить зависимости
make run        # Запустить бота
make dev        # Запустить в режиме разработки (DEBUG логи)
make lint       # Проверить код линтером
make format     # Форматировать код
```

### Конфигурация

Создайте файл `.env` в корне проекта со следующими параметрами:

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

## 📚 Документация

- [Концепция проекта](docs/idea.md) - описание идеи и назначения бота
- [Техническое видение](docs/vision.md) - детальная техническая документация, архитектура и руководство по разработке

## 🛠 Технологии

- **Python 3.11+** с асинхронностью (async/await)
- **aiogram 3.x** - фреймворк для Telegram Bot API
- **OpenRouter** - доступ к различным LLM моделям
- **uv** - управление зависимостями

## 📝 Лицензия

См. [LICENSE](LICENSE)
