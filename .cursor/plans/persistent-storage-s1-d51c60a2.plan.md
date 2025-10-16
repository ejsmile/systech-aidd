<!-- d51c60a2-a887-4587-bee8-ca328f83479c c13e8f7d-3976-4dff-8f53-fd3fb1bce7ec -->
# Реализация персистентного хранения (SP-1)

## Цель

Сохранение истории диалогов в PostgreSQL между перезапусками бота с поддержкой soft delete, даты создания и длины сообщений.

## Технические решения

- **СУБД:** PostgreSQL (через Docker)
- **ORM:** SQLAlchemy 2.x (async mode)
- **Миграции:** Alembic
- **Драйвер:** asyncpg
- **Схема:** Денормализованная (одна таблица messages)

## Структура данных

### Таблица messages

```sql
- id: BIGSERIAL PRIMARY KEY
- chat_id: BIGINT NOT NULL
- user_id: BIGINT NOT NULL
- role: VARCHAR(20) NOT NULL (system/user/assistant)
- content: TEXT NOT NULL
- content_length: INTEGER NOT NULL
- created_at: TIMESTAMP NOT NULL DEFAULT NOW()
- deleted_at: TIMESTAMP NULL

Индексы:
- idx_messages_lookup: (chat_id, user_id, deleted_at, created_at DESC)
- idx_messages_created: (created_at DESC)
```

## Ключевые файлы

### Новые файлы

- `docker-compose.yml` - PostgreSQL контейнер
- `src/database.py` - настройка SQLAlchemy engine и session
- `src/db_models.py` - SQLAlchemy модели (класс Message)
- `src/repository.py` - MessageRepository для работы с БД
- `alembic.ini` - конфигурация Alembic
- `alembic/env.py` - настройка миграций
- `alembic/versions/001_initial.py` - первая миграция

### Изменяемые файлы

- `pyproject.toml` - добавить sqlalchemy, alembic, asyncpg
- `src/config.py` - добавить database_url
- `src/conversation.py` - использовать MessageRepository вместо dict
- `src/main.py` - инициализация БД при старте
- `Makefile` - команды для Docker и миграций
- `sample.env` - добавить DATABASE_URL

## Пошаговый план

### 1. Docker и зависимости

- Создать `docker-compose.yml` с PostgreSQL и healthcheck
- Обновить `pyproject.toml` с зависимостями (sqlalchemy, alembic, asyncpg, testcontainers)
- Обновить `.env.example` с DATABASE_URL

### 2. Настройка SQLAlchemy

- Создать `src/database.py` с async engine и session factory
- Создать `src/db_models.py` с моделью Message (с soft delete, created_at, content_length)

### 3. Настройка Alembic

- Инициализировать Alembic: `alembic init alembic`
- Настроить `alembic.ini` и `alembic/env.py` для async
- Создать первую миграцию с таблицей messages и индексами
- Создать seed миграцию с тестовыми данными (2 пользователя, по 2-3 диалога, 10-15 сообщений)
- Обновить `docker-compose.yml`: добавить сервис для автоматического применения миграций при старте БД

### 4. Слой доступа к данным

- Создать `src/repository.py` с классом MessageRepository
- Методы: add_message, get_history, soft_delete_history, get_history_count
- Все методы асинхронные, используют soft delete фильтр

### 5. Рефакторинг ConversationManager

- Заменить dict на MessageRepository
- Сохранять content_length при добавлении сообщения
- При получении истории - фильтровать по deleted_at IS NULL
- При очистке - установить deleted_at = NOW()

### 6. Обновление конфигурации

- Добавить в Config поле database_url
- Обновить sample.env с примером DATABASE_URL

### 7. Обновление main.py

- Инициализация БД при старте
- Проверка подключения к БД
- Graceful shutdown с закрытием соединений

### 8. Makefile команды

- `make db-up` - запустить PostgreSQL
- `make db-down` - остановить PostgreSQL
- `make db-migrate` - применить миграции
- `make db-revision` - создать новую миграцию

### 9. Обновление тестов

- Использовать testcontainers-python с PostgreSQL для изоляции
- Создать fixture для тестового контейнера в conftest.py
- Автоматически применять все миграции при запуске тестовой БД
- Обновить тесты ConversationManager для работы с БД
- Добавить тесты для MessageRepository
- Добавить pytest-asyncio и testcontainers в dev-зависимости

## Важные моменты

### Soft Delete

- Поле `deleted_at` по умолчанию NULL
- При "удалении" устанавливается текущая timestamp
- Все запросы фильтруют `WHERE deleted_at IS NULL`

### Оптимизация

- Составной индекс (chat_id, user_id, deleted_at, created_at DESC) для быстрой выборки
- Денормализация: chat_id и user_id в каждой записи (без join'ов)
- Ограничение истории: LIMIT в запросе (вместо in-memory обрезки)

### Принцип KISS

- Одна таблица messages (без отдельных users/conversations)
- Простой MessageRepository без сложных паттернов
- Async везде (требование aiogram)
- Минимум абстракций

### To-dos

- [ ] Создать docker-compose.yml и обновить зависимости в pyproject.toml
- [ ] Создать database.py и db_models.py с SQLAlchemy моделями
- [ ] Настроить Alembic и создать первую миграцию
- [ ] Создать MessageRepository с методами для работы с БД
- [ ] Рефакторинг ConversationManager для использования MessageRepository
- [ ] Обновить Config и sample.env с database_url
- [ ] Обновить main.py для инициализации БД при старте
- [ ] Добавить команды в Makefile для Docker и миграций
- [ ] Обновить тесты для работы с БД
- [ ] Актуализировать vision.md и idea.md на соответствие сделанным изменениям
- [ ] Добавить ссылку на план в таблицу спринтов в roadmap.md