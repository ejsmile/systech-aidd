# Схема базы данных

## Обзор

Проект использует PostgreSQL 16 для хранения персистентных данных. Основные сущности:
- **messages** - история диалогов с пользователями
- **users** - профили пользователей Telegram

## Таблица: users

### Назначение
Хранение информации о пользователях Telegram, полученной через Bot API.

### Структура

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `user_id` | BIGINT | PRIMARY KEY | Уникальный идентификатор пользователя в Telegram |
| `username` | VARCHAR(255) | NULL | Username пользователя (без @) |
| `first_name` | VARCHAR(255) | NULL | Имя пользователя |
| `last_name` | VARCHAR(255) | NULL | Фамилия пользователя |
| `bio` | TEXT | NULL | Описание профиля (резерв на будущее) |
| `age` | INTEGER | NULL | Возраст пользователя (резерв на будущее) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Дата первого взаимодействия с ботом |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Дата последнего обновления данных |

### SQL определение

```sql
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255) NULL,
    first_name VARCHAR(255) NULL,
    last_name VARCHAR(255) NULL,
    bio TEXT NULL,
    age INTEGER NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

### Индексы

```sql
-- Индекс для быстрого поиска по username
CREATE INDEX idx_users_username ON users(username) WHERE username IS NOT NULL;

-- Индекс для поиска по дате создания
CREATE INDEX idx_users_created ON users(created_at DESC);
```

**Обоснование индексов:**
- `idx_users_username` - частичный индекс для поиска пользователей по username (только для NOT NULL значений)
- `idx_users_created` - для сортировки пользователей по дате регистрации

### Связи с другими таблицами

**messages.user_id → users.user_id**
- Тип: Foreign Key (будет добавлен в будущей миграции)
- Действие при удалении: CASCADE (при удалении пользователя удаляются его сообщения)
- Примечание: Foreign key не добавлен в текущей миграции для упрощения data-миграции

## Таблица: messages

### Назначение
Хранение истории диалогов между пользователями и LLM-ассистентом.

### Структура

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | BIGSERIAL | PRIMARY KEY | Уникальный идентификатор сообщения |
| `chat_id` | BIGINT | NOT NULL | ID чата в Telegram |
| `user_id` | BIGINT | NOT NULL | ID пользователя в Telegram |
| `role` | VARCHAR(20) | NOT NULL | Роль отправителя: system, user, assistant |
| `content` | TEXT | NOT NULL | Содержимое сообщения |
| `content_length` | INTEGER | NOT NULL | Длина сообщения в символах |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Время создания сообщения |
| `deleted_at` | TIMESTAMP | NULL | Время мягкого удаления (soft delete) |

### Индексы

```sql
-- Основной индекс для быстрой выборки истории диалога
CREATE INDEX idx_messages_lookup ON messages(chat_id, user_id, deleted_at, created_at DESC);

-- Индекс для сортировки по дате создания
CREATE INDEX idx_messages_created ON messages(created_at DESC);
```

### Soft Delete

Таблица `messages` использует паттерн **soft delete**:
- Удаленные сообщения имеют `deleted_at IS NOT NULL`
- Активные сообщения имеют `deleted_at IS NULL`
- При выборке истории всегда используется фильтр `WHERE deleted_at IS NULL`

## ER-диаграмма

```
┌─────────────────────────────────────┐
│            users                     │
├─────────────────────────────────────┤
│ PK  user_id       BIGINT            │
│     username      VARCHAR(255) NULL │
│     first_name    VARCHAR(255) NULL │
│     last_name     VARCHAR(255) NULL │
│     bio           TEXT NULL          │
│     age           INTEGER NULL       │
│     created_at    TIMESTAMP NOT NULL │
│     updated_at    TIMESTAMP NOT NULL │
└─────────────────────────────────────┘
             ▲
             │
             │ FK (планируется)
             │
┌─────────────────────────────────────┐
│          messages                    │
├─────────────────────────────────────┤
│ PK  id            BIGSERIAL          │
│     chat_id       BIGINT NOT NULL    │
│ FK  user_id       BIGINT NOT NULL    │ ───┘
│     role          VARCHAR(20)        │
│     content       TEXT               │
│     content_length INTEGER           │
│     created_at    TIMESTAMP          │
│     deleted_at    TIMESTAMP NULL     │
└─────────────────────────────────────┘
```

## Доступные поля Telegram User API

### Источник данных: aiogram.types.User

Telegram Bot API предоставляет следующие поля о пользователе через `message.from_user`:

| Поле | Тип | Обязательное | Описание | Используется |
|------|-----|--------------|----------|--------------|
| `id` | int | ✅ Да | Уникальный идентификатор пользователя | ✅ Да (→ user_id) |
| `first_name` | str | ✅ Да | Имя пользователя | ✅ Да |
| `last_name` | Optional[str] | ❌ Нет | Фамилия пользователя | ✅ Да |
| `username` | Optional[str] | ❌ Нет | Username (без @) | ✅ Да |
| `is_bot` | bool | ✅ Да | Флаг бота | ❌ Нет (можем добавить позже) |
| `language_code` | Optional[str] | ❌ Нет | IETF тег языка (en, ru) | ❌ Нет (можем добавить позже) |
| `is_premium` | Optional[bool] | ❌ Нет | Premium статус | ❌ Нет |

**Примечания:**
- Поля `bio` и `age` в таблице `users` - резерв на будущее, не доступны через Bot API
- `bio` можно получить только через расширенный метод `getChat()` для приватных чатов
- `age` нужно собирать вручную через диалог с пользователем

### Пример извлечения данных

```python
from aiogram.types import Message, User

async def extract_user_data(telegram_user: User) -> UserData:
    """Извлечь данные пользователя из Telegram объекта"""
    return UserData(
        user_id=telegram_user.id,
        username=telegram_user.username,
        first_name=telegram_user.first_name,
        last_name=telegram_user.last_name,
    )
```

### Edge cases

**Отсутствующие опциональные поля:**
- `username` может быть `None` - пользователь не установил username
- `last_name` может быть `None` - пользователь не указал фамилию

**Изменение данных:**
- Пользователь может изменить `username`, `first_name`, `last_name` в любой момент
- Стратегия: обновляем данные при каждом взаимодействии через `upsert`

## Стратегия миграции данных

### Текущее состояние

**Таблица messages:**
- Содержит 4 уникальных пользователя (user_id: 101, 202, 63536159, 999)
- Всего 30 сообщений в истории
- Данные о пользователях отсутствуют (username, first_name, last_name)

### План миграции

**Этап 1: Schema Migration**
1. Создать таблицу `users` с индексами
2. Не добавлять Foreign Key на `messages.user_id` (добавим позже)

**Этап 2: Data Migration**
1. Извлечь уникальные `user_id` из таблицы `messages`
2. Для каждого `user_id` создать запись в `users`:
   - `user_id` - из messages
   - `username`, `first_name`, `last_name` - NULL (заполнятся при следующем взаимодействии)
   - `created_at` - MIN(created_at) из messages для этого user_id
   - `updated_at` - CURRENT_TIMESTAMP

**Этап 3: Runtime Upsert**
При каждом сообщении от пользователя:
1. Извлечь данные из `message.from_user`
2. Выполнить UPSERT в таблицу `users`:
   - Если запись существует → обновить `username`, `first_name`, `last_name`, `updated_at`
   - Если запись не существует → создать новую со всеми данными

### SQL для Data Migration

```sql
-- Миграция существующих пользователей из messages
INSERT INTO users (user_id, username, first_name, last_name, created_at, updated_at)
SELECT DISTINCT 
    user_id,
    NULL as username,
    NULL as first_name, 
    NULL as last_name,
    MIN(created_at) as created_at,
    CURRENT_TIMESTAMP as updated_at
FROM messages
WHERE deleted_at IS NULL
GROUP BY user_id
ON CONFLICT (user_id) DO NOTHING;
```

### Стратегия обновления

**Частота обновления:**
- При каждом сообщении пользователя (команда или текст)
- Обновление выполняется ДО обработки сообщения

**Graceful degradation:**
- Если сохранение пользователя не удалось → логируем ошибку
- Бот продолжает работать (обработка сообщения не прерывается)

**UPSERT логика:**
```sql
INSERT INTO users (user_id, username, first_name, last_name, created_at, updated_at)
VALUES ($1, $2, $3, $4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
ON CONFLICT (user_id) DO UPDATE SET
    username = EXCLUDED.username,
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    updated_at = CURRENT_TIMESTAMP;
```

## Миграции Alembic

### Существующие миграции

1. `0b1d225cd32e` - Initial migration: create messages table
2. `9c0083885caf` - Seed test data

### Планируемые миграции

3. **add_users_table** (schema migration):
   - Создать таблицу `users`
   - Создать индексы `idx_users_username`, `idx_users_created`

4. **migrate_existing_users** (data migration):
   - Заполнить `users` данными из `messages`
   - Создать записи с базовыми данными (user_id, created_at)

5. **add_foreign_key_messages_users** (опционально, в будущем):
   - Добавить Foreign Key: `messages.user_id → users.user_id`

## Примечания по производительности

### Оптимизация запросов

**Получение истории с данными пользователя:**
```sql
SELECT m.*, u.username, u.first_name, u.last_name
FROM messages m
LEFT JOIN users u ON m.user_id = u.user_id
WHERE m.chat_id = $1 AND m.user_id = $2 AND m.deleted_at IS NULL
ORDER BY m.created_at DESC
LIMIT 20;
```

**Статистика по пользователям:**
```sql
SELECT u.user_id, u.username, u.first_name, COUNT(m.id) as message_count
FROM users u
LEFT JOIN messages m ON u.user_id = m.user_id AND m.deleted_at IS NULL
GROUP BY u.user_id, u.username, u.first_name
ORDER BY message_count DESC;
```

### Масштабирование

**Текущие объемы:**
- 4 пользователя
- 30 сообщений

**Ожидаемый рост:**
- До 1000 пользователей: индексы не критичны, текущая структура достаточна
- До 10000 пользователей: индексы начинают приносить пользу
- Более 100000 пользователей: рассмотреть партиционирование таблицы `messages` по дате

---

**Последнее обновление:** Итерация 1, SP-2 (октябрь 2025)

