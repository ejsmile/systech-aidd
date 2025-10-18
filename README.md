# systech-aidd

[![Build Status](https://github.com/ejsmile/systech-aidd/workflows/Build%20and%20Publish/badge.svg)](https://github.com/ejsmile/systech-aidd/actions)

LLM-ассистент в виде Telegram-бота для взаимодействия с пользователями через интеллектуальный диалог.

**Бот:** [@systtech_ai_bot_pk_bot](https://t.me/systtech_ai_bot_pk_bot)

## 🚀 Быстрый старт

## 🐳 Docker запуск (рекомендуется)

Самый простой способ запустить весь проект:

### Требования
- Docker
- Docker Compose
- Файл `.env` с токенами (скопировать из `sample.env`)

### Запуск
```bash
# 1. Клонировать репозиторий
git clone <repository-url>
cd systech-aidd-my

# 2. Настроить .env файл
cp sample.env .env
# Отредактировать .env и добавить токены

# 3. Запустить все сервисы
docker-compose up

# Или в фоновом режиме
docker-compose up -d
```

### Доступ к сервисам
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173
- **PostgreSQL:** localhost:5433
- **Telegram Bot:** автоматически подключается

### Полезные команды
```bash
# Остановить все сервисы
docker-compose down

# Пересобрать образы (после изменения кода)
docker-compose up --build

# Посмотреть логи
docker-compose logs -f

# Посмотреть логи конкретного сервиса
docker-compose logs -f bot
docker-compose logs -f api

# Перезапустить сервис
docker-compose restart bot

# Очистить всё (включая volumes)
docker-compose down -v
```

---

## 🐳 Использование Docker образов из Registry

Вместо локальной сборки образов можно использовать готовые образы из GitHub Container Registry (ghcr.io).

### Преимущества

- ✅ Не нужно собирать образы локально (экономия времени)
- ✅ Быстрый старт проекта
- ✅ Гарантированно рабочие образы из main ветки
- ✅ Образы публичные - доступны без авторизации

### Использование

```bash
# Запуск через образы из registry
docker-compose -f docker-compose.registry.yml up

# Или в фоновом режиме
docker-compose -f docker-compose.registry.yml up -d

# Обновить образы до последней версии
docker-compose -f docker-compose.registry.yml pull
docker-compose -f docker-compose.registry.yml up -d
```

### Pull образов вручную

```bash
# Bot/API образ (один образ для bot и api)
docker pull ghcr.io/ejsmile/systech-aidd-bot:latest

# API образ
docker pull ghcr.io/ejsmile/systech-aidd-api:latest

# Frontend образ
docker pull ghcr.io/ejsmile/systech-aidd-frontend:latest
```

### Доступные теги

- `latest` - последняя стабильная версия из main ветки
- `sha-<commit>` - конкретный commit (например `sha-abc1234`)

### Когда использовать?

**Используйте образы из registry:**
- Для быстрого старта проекта
- Для тестирования последней версии
- Для production деплоя

**Используйте локальную сборку:**
- При разработке новых фич
- При отладке Dockerfile
- При тестировании изменений до commit

---

## 💻 Локальная разработка (без Docker)

### Требования

**Backend:**
- **Python 3.11+** - требуемая версия
- **[uv](https://github.com/astral-sh/uv)** - менеджер пакетов и виртуальных окружений
- **Docker & Docker Compose** - для PostgreSQL
- **Telegram Bot Token** - получить у [@BotFather](https://t.me/botfather)
- **OpenRouter API Key** - получить на [openrouter.ai](https://openrouter.ai)

**Frontend:**
- **Node.js 18+** - для npm и запуска frontend
- **npm** - менеджер пакетов (устанавливается с Node.js)

### Установка и запуск

**Backend:**
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

# 5. Запустить бота или API
make run        # Telegram бот
# или
make run-api    # API сервер (http://localhost:8000)
```

**Frontend (опционально):**
```bash
# 1. Установить зависимости
make frontend-install

# 2. Настроить переменные окружения (создать frontend/.env)
echo "VITE_API_BASE_URL=http://localhost:8000/api/v1" > frontend/.env

# 3. Запустить dev сервер
make frontend-dev   # откроется на http://localhost:5173
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

# Frontend (веб-интерфейс)
make frontend-install  # Установить зависимости
make frontend-dev      # Запустить dev сервер (http://localhost:5173)
make frontend-build    # Собрать для продакшена
make frontend-test     # Запустить тесты
make frontend-lint     # Линтинг кода
make frontend-format   # Форматирование кода

# Качество кода
make quality       # Backend: format + lint + typecheck
make frontend-quality  # Frontend: format + lint
make quality-all   # Backend + Frontend: полная проверка качества

# Тестирование
make test          # Backend тесты (env vars из conftest.py)
make test-cov      # Backend тесты с coverage отчетом
make test-docker   # Backend тесты в Docker (изолированное окружение)
make frontend-test # Frontend тесты (Vitest + jsdom)

# Разработка
make install-dev   # Установить dev-зависимости
make clean         # Очистить временные файлы
```

Полный список команд см. в [Makefile](Makefile)

## 📁 Структура проекта

```
systech-aidd-my/
├── src/                   # Backend исходный код (1 класс = 1 файл)
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
│       ├── app.py        # FastAPI приложение и endpoints
│       ├── models.py     # Pydantic модели для API
│       ├── chat_handler.py       # WebChatHandler для чата
│       ├── text2sql_handler.py   # Text2SQLHandler для SQL запросов
│       ├── stat_collector.py     # Protocol для статистики
│       └── mock_stat_collector.py # Mock реализация
├── frontend/             # Frontend исходный код (React + TypeScript)
│   ├── src/              # Исходный код приложения
│   │   ├── components/   # Переиспользуемые компоненты
│   │   │   ├── FloatingChat.tsx       # Обертка floating чата
│   │   │   ├── FloatingChatButton.tsx # Кнопка чата в правом нижнем углу
│   │   │   ├── FloatingChatWindow.tsx # Окно чата
│   │   │   ├── ui/       # Shadcn/ui компоненты (button, card, chat-input, etc.)
│   │   │   └── ...       # Другие компоненты (MetricCard, Charts, etc.)
│   │   ├── pages/        # Страницы (Dashboard)
│   │   ├── api/          # API клиент для backend
│   │   ├── types/        # TypeScript типы
│   │   ├── hooks/        # Custom React hooks (use-textarea-resize)
│   │   ├── contexts/     # React Context (ThemeContext)
│   │   └── lib/          # Утилиты
│   ├── docs/             # Frontend документация
│   ├── package.json      # Зависимости и скрипты
│   └── vite.config.ts    # Конфигурация Vite
├── alembic/              # Миграции базы данных
├── tests/                # Автоматизированные тесты (105 тестов, coverage >85%)
├── docs/                 # Общая документация
│   ├── api/              # API документация
│   └── frontend/         # Frontend требования
├── docker-compose.yml    # PostgreSQL для разработки (настройки подключения)
├── Dockerfile.migrations # Docker для автоматических миграций
├── Makefile             # Команды разработки
└── pyproject.toml       # Конфигурация backend
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

### Frontend
- **React 18** - UI библиотека
- **TypeScript 5** - type safety
- **Vite** - быстрая сборка и dev сервер
- **Tailwind CSS** - utility-first стилизация
- **Shadcn/ui** - современные UI компоненты
- **Recharts** - декларативные графики
- **React Router** - клиентский роутинг

**Возможности:**
- **Floating AI Chat** - глобальный чат-помощник в правом нижнем углу
  - Два режима: обычный (LLM) и админ (Text2SQL)
  - Badge индикатор режима (AI/SQL)
  - Адаптивный дизайн (desktop: floating окно, mobile: full screen)
  - История диалогов с автоскроллом
- **Dashboard Analytics** - визуализация статистики использования бота
- **Dark/Light Theme** - поддержка темной и светлой темы
- **Period Filtering** - фильтрация статистики по периодам

### Infrastructure
- **Docker Compose** - локальная инфраструктура
- **uv** - управление зависимостями (backend)
- **npm** - управление зависимостями (frontend)
- **uvicorn** - ASGI сервер для FastAPI

### Quality & Testing
**Backend:**
- **ruff** - линтинг и форматирование
- **mypy (strict mode)** - проверка типов
- **pytest + pytest-asyncio** - тестирование
- **testcontainers** - изолированные тесты с реальной БД
- **Coverage >85%** - 105 тестов

**Frontend:**
- **ESLint** - линтинг JavaScript/TypeScript
- **Prettier** - форматирование кода
- **TypeScript strict mode** - проверка типов
- **Vitest** - unit тестирование
- **React Testing Library** - тестирование компонентов

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
# Backend
make quality       # format + lint + typecheck

# Frontend
make frontend-quality  # format + lint

# Всё вместе
make quality-all   # Backend + Frontend полная проверка

# Тестирование
make test          # Backend тесты
make test-cov      # Backend тесты с coverage отчетом
make frontend-test # Frontend тесты

# Полная проверка перед коммитом
make quality-all && make test && make frontend-test
```

Workflow разработки см. в [.cursor/rules/workflow.mdc](.cursor/rules/workflow.mdc)

## 📚 Документация

### Основная
- **[docs/idea.md](docs/idea.md)** - концепция проекта
- **[docs/vision.md](docs/vision.md)** - техническое видение и архитектура
- **[docs/roadmap.md](docs/roadmap.md)** - роадмап и спринты проекта
- **[docs/database_schema.md](docs/database_schema.md)** - схема базы данных (таблицы, индексы, связи)

### DevOps
- **[devops/doc/devops-roadmap.md](devops/doc/devops-roadmap.md)** - DevOps roadmap (Docker, CI/CD, деплой)

### API для веб-интерфейса
- **[docs/api/api-contract.md](docs/api/api-contract.md)** - API контракт и endpoints
- **[docs/frontend/dashboard-requirements.md](docs/frontend/dashboard-requirements.md)** - требования к дашборду
- **http://localhost:8000/docs** - интерактивная OpenAPI документация (после `make run-api`)

### Frontend
- **[frontend/docs/front-vision.md](frontend/docs/front-vision.md)** - видение frontend приложения
- **[frontend/docs/tech-stack.md](frontend/docs/tech-stack.md)** - технологический стек frontend
- **http://localhost:5173** - dev сервер (после `make frontend-dev`)

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
