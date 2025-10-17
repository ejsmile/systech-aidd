# Техническое видение проекта

## 1. Технологии

### Backend Stack
- **Python 3.11+** - язык программирования
- **uv** - управление зависимостями и виртуальным окружением
- **aiogram 3.x** - асинхронный фреймворк для Telegram Bot API (метод polling)
- **FastAPI** - REST API для веб-интерфейса
- **openai** - клиент для работы с LLM через провайдер OpenRouter
- **make** - автоматизация задач сборки и запуска

### Frontend Stack
- **React 18** - UI библиотека
- **TypeScript 5** - type safety для JavaScript
- **Vite 7** - быстрая сборка и dev сервер
- **Tailwind CSS 4** - utility-first CSS фреймворк
- **Shadcn/ui** - современные UI компоненты (Radix UI + Tailwind)
- **Recharts** - декларативные графики для React
- **React Router 6** - клиентский роутинг
- **npm** - управление зависимостями frontend

### Дополнительные библиотеки (Backend)
- **pydantic** - валидация данных
- **pydantic-settings** - загрузка и валидация конфигурации из переменных окружения
- **python-dotenv** - работа с .env файлами
- **dataclasses** (стандартная библиотека Python) - классы данных
- **logging** (стандартная библиотека Python) - логирование

### Инструменты качества кода

**Backend (dev-зависимости):**
- **ruff** - быстрый форматтер и линтер (замена black, isort, flake8)
- **mypy** - статическая проверка типов (strict mode)
- **pytest** - фреймворк для тестирования
- **pytest-asyncio** - поддержка async тестов
- **pytest-cov** - измерение покрытия кода тестами
- **testcontainers** - изоляция тестов с реальной БД

**Frontend (dev-зависимости):**
- **ESLint** - линтинг JavaScript/TypeScript
- **Prettier** - форматирование кода
- **TypeScript strict mode** - строгая проверка типов
- **Vitest** - unit тестирование (совместим с Vite)
- **React Testing Library** - тестирование React компонентов

### Хранение данных
- **PostgreSQL 16** - персистентное хранение истории диалогов и пользователей
- **SQLAlchemy 2.x (async)** - ORM для работы с БД
- **Alembic** - система миграций
- **asyncpg** - асинхронный драйвер PostgreSQL
- **Docker Compose** - запуск PostgreSQL локально (настройки в `docker-compose.yml`)
- **testcontainers** - изоляция тестов с реальной БД

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
├── src/                    # Backend исходный код
│   ├── __init__.py
│   ├── main.py            # Точка входа для Telegram бота
│   ├── bot.py             # Класс Bot - инициализация aiogram
│   ├── handlers.py        # Обработка сообщений и команд из Telegram
│   ├── llm_client.py      # Класс LLMClient - работа с OpenRouter
│   ├── conversation.py    # Класс ConversationManager - управление историей
│   ├── models.py          # Классы данных: ConversationKey, ChatMessage, Role, UserData
│   ├── config.py          # Класс Config - конфигурация
│   ├── database.py        # Класс Database - управление подключением к БД
│   ├── db_models.py       # SQLAlchemy модели (Message, User)
│   ├── repository.py      # MessageRepository - слой доступа к данным
│   ├── user_repository.py # UserRepository - работа с пользователями
│   └── api/               # FastAPI веб-интерфейс
│       ├── __init__.py
│       ├── main.py        # Точка входа для API сервера
│       ├── app.py         # FastAPI приложение
│       ├── models.py      # Pydantic модели для API
│       ├── stat_collector.py     # Protocol для статистики
│       └── mock_stat_collector.py # Mock реализация
├── frontend/             # Frontend исходный код
│   ├── docs/             # Frontend документация
│   │   ├── front-vision.md    # Видение frontend приложения
│   │   └── tech-stack.md      # Технологический стек
│   ├── src/              # Исходный код приложения
│   │   ├── components/   # Переиспользуемые компоненты
│   │   │   ├── ui/       # Shadcn/ui компоненты
│   │   │   └── SampleChart.tsx  # Пример графика
│   │   ├── pages/        # Страницы (Dashboard, Chat)
│   │   │   ├── Dashboard.tsx
│   │   │   └── Chat.tsx
│   │   ├── api/          # API клиент для backend
│   │   │   ├── client.ts
│   │   │   └── statistics.ts
│   │   ├── types/        # TypeScript типы
│   │   │   └── statistics.ts
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Утилиты
│   │   │   └── utils.ts  # cn() для Tailwind
│   │   ├── App.tsx       # Главный компонент с роутингом
│   │   ├── App.test.tsx  # Тесты для App
│   │   ├── main.tsx      # Entry point
│   │   ├── index.css     # Tailwind CSS imports
│   │   └── setupTests.ts # Настройка тестов
│   ├── public/           # Статические файлы
│   ├── package.json      # Зависимости и скрипты
│   ├── tsconfig.json     # TypeScript конфигурация
│   ├── vite.config.ts    # Vite + Vitest конфигурация
│   ├── tailwind.config.js # Tailwind CSS конфигурация
│   ├── postcss.config.js # PostCSS конфигурация
│   ├── .prettierrc       # Prettier конфигурация
│   ├── eslint.config.js  # ESLint конфигурация
│   └── components.json   # Shadcn/ui конфигурация
├── prompts/               # Файлы системных промптов
│   └── system.txt         # Системный промпт (роль ассистента)
├── tests/                 # Backend автоматизированные тесты
│   ├── __init__.py
│   ├── conftest.py        # Общие fixtures
│   ├── test_models.py     # Тесты моделей данных
│   ├── test_conversation.py  # Тесты ConversationManager
│   ├── test_llm_client.py    # Тесты LLMClient
│   ├── test_config.py        # Тесты конфигурации
│   ├── test_repository.py    # Тесты MessageRepository
│   ├── test_user_repository.py  # Тесты UserRepository
│   ├── test_handlers.py      # Тесты обработчиков
│   ├── test_database.py      # Тесты Database
│   ├── test_integration.py   # Интеграционные тесты
│   ├── test_user_integration.py  # Интеграционные тесты пользователей
│   ├── test_api_endpoints.py    # Тесты API endpoints
│   ├── test_api_models.py       # Тесты API моделей
│   └── test_mock_stat_collector.py # Тесты MockStatCollector
├── alembic/              # Миграции базы данных
│   ├── versions/         # Файлы миграций
│   └── env.py            # Настройка Alembic
├── docs/                 # Общая документация
│   ├── api/              # API документация
│   │   └── api-contract.md
│   ├── frontend/         # Frontend требования
│   │   └── dashboard-requirements.md
│   ├── idea.md
│   ├── vision.md
│   ├── roadmap.md         # Роадмап проекта
│   ├── database_schema.md # Схема базы данных
│   └── tasklists/        # Детальные планы спринтов
├── .env.example          # Пример конфигурации
├── .gitignore
├── alembic.ini           # Конфигурация Alembic
├── docker-compose.yml    # PostgreSQL контейнер (настройки подключения к БД)
├── Dockerfile.migrations # Docker образ для автоматических миграций
├── Makefile              # Команды для сборки, запуска и тестирования (Backend + Frontend)
├── pyproject.toml        # Конфигурация backend проекта
├── uv.lock               # Backend lockfile с точными версиями зависимостей
└── README.md
```

### Описание ключевых файлов

**Backend исходный код:**
- **main.py** - запуск бота, инициализация БД, связывание компонентов, загрузка системного промпта
- **bot.py** - создание и настройка aiogram Bot и Dispatcher
- **handlers.py** - обработка входящих сообщений и команд из Telegram (`/start`, `/help`, `/clear`, `/role`)
- **llm_client.py** - отправка запросов к LLM через OpenRouter
- **conversation.py** - управление историей диалога через MessageRepository
- **models.py** - классы данных (ConversationKey, ChatMessage, Role, UserData)
- **config.py** - загрузка и валидация конфигурации
- **database.py** - управление подключением к PostgreSQL
- **db_models.py** - SQLAlchemy модели (Message с soft delete, User)
- **repository.py** - MessageRepository для работы с сообщениями
- **user_repository.py** - UserRepository для работы с пользователями

**API (FastAPI):**
- **api/main.py** - точка входа для API сервера (uvicorn)
- **api/app.py** - FastAPI приложение с endpoints и CORS
- **api/models.py** - Pydantic модели для валидации API запросов/ответов
- **api/stat_collector.py** - Protocol интерфейс для сборщика статистики
- **api/mock_stat_collector.py** - Mock реализация для разработки frontend

**Frontend (React + TypeScript):**
- **App.tsx** - главный компонент с роутингом и sidebar навигацией
- **pages/Dashboard.tsx** - страница дашборда со статистикой
- **pages/Chat.tsx** - страница веб-чата с ботом
- **api/client.ts** - базовый HTTP клиент для запросов к backend API
- **api/statistics.ts** - методы для получения статистики
- **types/statistics.ts** - TypeScript типы для API моделей
- **lib/utils.ts** - утилита cn() для работы с Tailwind CSS классами
- **components/SampleChart.tsx** - пример компонента с графиком Recharts

**Промпты:**
- **prompts/system.txt** - системный промпт, определяющий роль и поведение ассистента (опционально, есть дефолт)

**Backend тестирование:**
- **conftest.py** - общие fixtures для переиспользования (testcontainers, session factory)
- **test_models.py** - unit-тесты моделей данных (ChatMessage, UserData)
- **test_conversation.py** - unit-тесты управления историей
- **test_llm_client.py** - unit-тесты LLM клиента (с mock'ами)
- **test_config.py** - тесты валидации конфигурации
- **test_repository.py** - unit-тесты MessageRepository
- **test_user_repository.py** - unit-тесты UserRepository
- **test_handlers.py** - unit-тесты обработчиков
- **test_database.py** - тесты Database (connection pooling, sessions)
- **test_integration.py** - интеграционные тесты полного цикла
- **test_user_integration.py** - интеграционные тесты работы с пользователями
- **test_api_endpoints.py** - тесты API endpoints (FastAPI)
- **test_api_models.py** - тесты валидации API моделей
- **test_mock_stat_collector.py** - тесты MockStatCollector

**Frontend тестирование:**
- **App.test.tsx** - unit-тесты главного компонента (Vitest + React Testing Library)
- Frontend тесты запускаются через `make frontend-test`

**Конфигурация:**
- **pyproject.toml** - метаданные проекта, зависимости, настройки инструментов (ruff, mypy, pytest)
- **uv.lock** - lockfile с точными версиями всех зависимостей (создаётся автоматически)
- **docker-compose.yml** - настройки PostgreSQL контейнера (user, password, database, port)
- **alembic.ini** - конфигурация системы миграций
- **.env** - переменные окружения (не в git, см. .env.example)

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
    "sqlalchemy[asyncio]>=2.0.0",
    "alembic>=1.13.0",
    "asyncpg>=0.29.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.4.0",
    "mypy>=1.10.0",
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
    "testcontainers>=4.0.0",
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

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

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
[Handlers] (handlers.py)
      ↓                  ↓
[UserRepository] ←  [ConversationManager] (conversation.py) ←→ [LLMClient] (llm_client.py)
      ↓                          ↓                                       ↓
      ↓                [MessageRepository] (repository.py)      OpenRouter API
      ↓                          ↓
      └──────────────→ [PostgreSQL Database] ←─────────────┘
                       (tables: users, messages)
```

### Поток обработки сообщения
1. **При запуске** бот загружает системный промпт из файла `prompts/system.txt` (или использует дефолт, если файл не найден)
2. **Пользователь** отправляет сообщение в Telegram
3. **Bot** (aiogram) получает сообщение через polling
4. **Handler** обрабатывает входящее сообщение
5. **UserRepository** сохраняет/обновляет данные пользователя (upsert)
6. **ConversationManager** добавляет сообщение в историю диалога
7. **LLMClient** отправляет историю + системный промпт в OpenRouter
8. **OpenRouter** возвращает ответ от LLM
9. **ConversationManager** добавляет ответ в историю
10. **Handler** отправляет ответ пользователю через Bot

### Ответственности классов
- **Config** - хранит конфигурацию (токены, URL, параметры LLM, путь к файлу промпта, database_url)
- **Bot** - обертка над aiogram Bot + Dispatcher, регистрация handlers
- **Handlers** - обработка команд (`/start`, `/help`, `/clear`, `/role`) и текстовых сообщений
- **ConversationManager** - управление историей диалогов через MessageRepository
- **LLMClient** - асинхронные запросы к OpenRouter API
- **Database** - управление async engine и session factory для PostgreSQL
- **Message (db_models)** - SQLAlchemy модель сообщения с soft delete
- **User (db_models)** - SQLAlchemy модель пользователя (user_id, username, first_name, last_name, bio, age)
- **MessageRepository** - CRUD операции с сообщениями (add_message, get_history, soft_delete_history)
- **UserRepository** - CRUD операции с пользователями (upsert_user, get_user_by_id, get_user_message_count)
- **ConversationKey** - immutable ключ для идентификации диалога (chat_id + user_id)
- **ChatMessage** - структура сообщения (role + content), формат совместим с OpenAI API
- **UserData** - структура данных пользователя из Telegram (user_id, username, first_name, last_name)
- **Role** - enum для валидации ролей (system, user, assistant)

## 5. Модель данных

### Конфигурация (Config)
```python
telegram_token: str          # Токен Telegram бота
openrouter_api_key: str      # API ключ OpenRouter
database_url: str            # URL подключения к PostgreSQL
                             # По умолчанию: "postgresql+asyncpg://aidd_user:aidd_password@localhost:5433/aidd_db"
                             # Параметры (user, password, db, port) смотри в docker-compose.yml
openrouter_base_url: str     # URL OpenRouter (по умолчанию: "https://openrouter.ai/api/v1")
model_name: str              # Название модели (например: "openai/gpt-oss-20b:free")
system_prompt_file: str      # Путь к файлу с системным промптом (по умолчанию: "prompts/system.txt")
system_prompt: str           # Системный промпт (загружается из файла или дефолт: "Ты полезный ассистент.")
max_history_messages: int    # Максимум сообщений в истории (по умолчанию: 20)
temperature: float           # Температура генерации LLM (по умолчанию: 0.7)
log_level: str               # Уровень логирования (по умолчанию: "INFO")
```

### База данных

**Таблицы:**
```python
# Классы данных:
@dataclass(frozen=True)
class ConversationKey:
    chat_id: int
    user_id: int

@dataclass(frozen=True)
class UserData:
    """Данные пользователя из Telegram"""
    user_id: int
    username: str | None
    first_name: str
    last_name: str | None

class Role(str, Enum):
    """Роли участников диалога"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

@dataclass
class ChatMessage:
    role: Literal["system", "user", "assistant"]
    content: str
    
    def to_dict(self) -> dict[str, str]:
        """Конвертация в формат OpenAI API"""
        return {"role": self.role, "content": self.content}

# SQLAlchemy модели:
class User(Base):
    """Модель пользователя Telegram"""
    user_id: int (BIGINT PRIMARY KEY)
    username: str | None (VARCHAR(255) UNIQUE NULLABLE)
    first_name: str | None (VARCHAR(255) NULLABLE)
    last_name: str | None (VARCHAR(255) NULLABLE)
    bio: str | None (TEXT NULLABLE)
    age: int | None (INTEGER NULLABLE)
    created_at: datetime (TIMESTAMP NOT NULL DEFAULT NOW())
    updated_at: datetime (TIMESTAMP NOT NULL DEFAULT NOW())

# Индексы users:
# - idx_users_username: (username) для быстрого поиска
# - idx_users_created: (created_at DESC) для сортировки

class Message(Base):
    """Модель сообщения в диалоге"""
    id: int (BIGSERIAL PRIMARY KEY)
    chat_id: int (BIGINT NOT NULL)
    user_id: int (BIGINT NOT NULL)
    role: str (VARCHAR(20) NOT NULL)
    content: str (TEXT NOT NULL)
    content_length: int (INTEGER NOT NULL)
    created_at: datetime (TIMESTAMP NOT NULL DEFAULT NOW())
    deleted_at: datetime | None (TIMESTAMP NULL)  # Soft delete

# Индексы messages:
# - idx_messages_lookup: (chat_id, user_id, deleted_at, created_at DESC)
# - idx_messages_created: (created_at DESC)

# Хранение: PostgreSQL 16
# Связи: User ←→ Message (по user_id, без foreign key для упрощения)
# Стратегия удаления: Soft delete для messages (deleted_at IS NULL для активных)
# Ограничение: последние 20 сообщений (+ system prompt) через LIMIT в SQL
# Миграции: Alembic (автоматические через Docker при старте)
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

### Сценарий 4: Отображение роли (`/role`)
1. Пользователь отправляет команду `/role`
2. Бот отправляет системный промпт, определяющий его роль
3. Пользователь видит, какую функцию выполняет ассистент

### Сценарий 5: Справка (`/help`)
1. Пользователь отправляет команду `/help`
2. Бот отправляет список доступных команд:
   - `/start` - начать работу
   - `/clear` - очистить историю диалога
   - `/role` - показать роль ассистента
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

# База данных
# Параметры подключения (user, password, db, port) смотри в docker-compose.yml
DATABASE_URL=postgresql+asyncpg://aidd_user:aidd_password@localhost:5433/aidd_db

# Необязательные (с значениями по умолчанию)
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
MODEL_NAME=openai/gpt-oss-20b:free
SYSTEM_PROMPT_FILE=prompts/system.txt
MAX_HISTORY_MESSAGES=20
TEMPERATURE=0.7
LOG_LEVEL=INFO
```

**Важно:** Параметры подключения к PostgreSQL (user, password, database, port) настраиваются в `docker-compose.yml`. 
По умолчанию:
- User: `aidd_user`
- Password: `aidd_password`
- Database: `aidd_db`
- Port: `5433` (внешний), `5432` (внутри контейнера)

### Валидация конфигурации
- Загрузка через `pydantic_settings.BaseSettings` (Pydantic v2)
- Валидация при старте приложения (fail-fast принцип)
- Если обязательные переменные не заданы → приложение не запускается с понятным сообщением об ошибке
- Системный промпт: если файл не существует, используется дефолтное значение ("Ты полезный ассистент.")

### Использование в коде
```python
config = Config()  # Автоматически загружает из .env

# Загрузка системного промпта из файла (с fallback на дефолт)
try:
    with open(config.system_prompt_file, "r", encoding="utf-8") as f:
        system_prompt = f.read().strip()
except FileNotFoundError:
    system_prompt = "Ты полезный ассистент."
    logger.warning(f"Файл промпта не найден, используется дефолтный")

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

## 10. Контроль качества и тестирование

### Автоматизированные инструменты

**Форматирование и линтинг (ruff):**
- Автоматическое форматирование кода (замена black + isort)
- Проверка стиля и потенциальных ошибок
- Настройка: line-length=100, target-version=py311
- Правила: E, F, I, N, W, UP, B, C90, PL

**Проверка типов (mypy):**
- Статическая проверка типов
- Режим: strict mode для максимальной type safety
- Требование: все функции с type hints
- Цель: предотвращение runtime ошибок на этапе разработки

**Тестирование (pytest):**
- Unit-тесты для критичных компонентов
- Интеграционные тесты для полного цикла работы
- Поддержка async/await через pytest-asyncio
- Измерение покрытия через pytest-cov

### Стратегия тестирования

**Приоритет покрытия:**
1. **Модели данных** - ConversationKey, ChatMessage, Role
2. **Бизнес-логика** - ConversationManager (история диалогов)
3. **Интеграция** - LLMClient (с mock'ами API)
4. **Конфигурация** - Config (валидация fail-fast)
5. **Полный цикл** - интеграционные тесты сценариев

**Принципы:**
- Тесты изолированные и быстрые
- Минимум mock'ов (только для внешних API)
- Понятные названия тестов (test_что_должно_происходить)
- Fixtures для переиспользуемых данных
- Цель покрытия: >80% для критичных модулей

**Что НЕ тестируем избыточно:**
- Тривиальные getters/setters
- Код фреймворка (aiogram, openai)
- Простые проксирующие методы

### Процесс контроля качества

**Backend - перед коммитом:**
1. `make format` - автоформатирование кода (ruff)
2. `make lint` - проверка линтером (ruff)
3. `make typecheck` - проверка типов (mypy strict)
4. `make test` - запуск тестов (pytest)

**Frontend - перед коммитом:**
1. `make frontend-format` - автоформатирование кода (Prettier)
2. `make frontend-lint` - проверка линтером (ESLint)
3. `make frontend-test` - запуск тестов (Vitest)

**Быстрая проверка:**
- `make quality` - Backend: format + lint + typecheck
- `make frontend-quality` - Frontend: format + lint
- `make quality-all` - Backend + Frontend полная проверка
- `make test-cov` - Backend тесты с отчетом о покрытии

**Полная проверка перед коммитом:**
```bash
make quality-all && make test && make frontend-test
```

**CI/CD готовность:**
- Все команды интегрируются в GitHub Actions
- Запуск на каждый push/PR
- Блокировка merge при провале проверок
- Backend coverage >85%, Frontend coverage target >70%

## 11. Локальная разработка

### Требования к окружению

**Backend:**
- **Python 3.11+** - установленный интерпретатор Python
- **uv** - менеджер пакетов и виртуальных окружений
- **Docker** - для запуска PostgreSQL (настройки в `docker-compose.yml`)
- **Telegram Bot Token** - получить через [@BotFather](https://t.me/botfather)
- **OpenRouter API Key** - получить на [openrouter.ai](https://openrouter.ai)

**Frontend:**
- **Node.js 18+** - для npm и запуска frontend
- **npm** - менеджер пакетов для JavaScript

**Общее:**
- **make** - для автоматизации команд (опционально, но рекомендуется)

### Установка и запуск

**Backend:**
1. Создать виртуальное окружение: `uv venv`
2. Установить зависимости: `uv pip install -e ".[dev]"` или `make install-dev`
3. Настроить `.env` файл:
   - Обязательные: `TELEGRAM_TOKEN`, `OPENROUTER_API_KEY`
   - `DATABASE_URL` - параметры подключения смотри в `docker-compose.yml`
4. Запустить PostgreSQL: `make db-up` (использует настройки из `docker-compose.yml`)
5. Применить миграции: `make db-migrate`
6. Запустить бота: `make run` (или API: `make run-api`)

**Frontend:**
1. Установить зависимости: `make frontend-install` (или `cd frontend && npm install`)
2. Настроить `.env` файл в `frontend/`:
   - `VITE_API_BASE_URL=http://localhost:8000/api/v1`
3. Запустить dev сервер: `make frontend-dev` (откроется на http://localhost:5173)

**Примечание:** 
- PostgreSQL запускается в Docker контейнере с настройками из `docker-compose.yml`
- Убедитесь, что порты 5433 (PostgreSQL), 8000 (API), 5173 (Frontend) свободны

### Команды Makefile

**Backend - Запуск:**
- `make install` - установить зависимости
- `make install-dev` - установить с dev-зависимостями (ruff, mypy, pytest, testcontainers)
- `make run` - запустить Telegram бота
- `make dev` - запустить в режиме разработки (LOG_LEVEL=DEBUG)
- `make run-api` - запустить API сервер (http://localhost:8000)

**Frontend - Запуск:**
- `make frontend-install` - установить зависимости
- `make frontend-dev` - запустить dev сервер (http://localhost:5173)
- `make frontend-build` - собрать для продакшена
- `make frontend-preview` - preview production build

**База данных:**
- `make db-up` - запустить PostgreSQL через Docker (настройки из `docker-compose.yml`)
- `make db-down` - остановить PostgreSQL
- `make db-migrate` - применить миграции (автоматически при `make db-up`)
- `make db-revision` - создать новую миграцию (m="description")
- `make db-reset` - полный сброс БД и повторное применение миграций

**Примечание:** Все параметры подключения к PostgreSQL (user, password, database, port) настраиваются в `docker-compose.yml`.

**Качество кода:**
- `make quality` - Backend: format + lint + typecheck
- `make frontend-quality` - Frontend: format + lint
- `make quality-all` - Backend + Frontend: полная проверка
- `make format` - Backend форматирование (ruff)
- `make lint` - Backend линтинг (ruff)
- `make typecheck` - Backend проверка типов (mypy)
- `make frontend-format` - Frontend форматирование (Prettier)
- `make frontend-lint` - Frontend линтинг (ESLint)

**Тестирование:**
- `make test` - Backend тесты (pytest с testcontainers)
- `make test-cov` - Backend тесты с отчетом о покрытии
- `make frontend-test` - Frontend тесты (Vitest)

**Прочее:**
- `make clean` - очистить временные файлы

### Режим отладки
Для детального логирования установить `LOG_LEVEL=DEBUG` в `.env` или через переменную окружения.

⚠️ **Важно:** DEBUG режим логирует содержимое сообщений - не используйте в продакшене!

---

## Итого

Документ технического видения проекта завершен. Все разделы описывают минимальное простое решение для проверки идеи согласно принципам KISS и ООП.

