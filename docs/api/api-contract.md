# API Contract - AIDD API

> **Базовый документ:** [roadmap.md](../roadmap.md)

## Обзор

AIDD API предоставляет REST endpoints для веб-интерфейса дашборда и чата. API построен на FastAPI и следует принципам REST.

**Base URL:** `http://localhost:8000`

**OpenAPI документация:** `http://localhost:8000/docs`

## Аутентификация

В текущей версии (v0.1.0) аутентификация не требуется. Будет добавлена в будущих версиях.

## Endpoints

### 1. Root Endpoint

**GET** `/`

Корневой endpoint для проверки работоспособности API.

**Response:**
```json
{
  "message": "AIDD API is running",
  "version": "0.1.0"
}
```

**Status codes:**
- `200 OK` - API работает

---

### 2. Health Check

**GET** `/health`

Health check endpoint для мониторинга.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status codes:**
- `200 OK` - Сервис здоров

---

### 3. Get Statistics

**GET** `/api/v1/statistics`

Получить статистику диалогов для дашборда.

**Query Parameters:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `start_date` | `datetime` (ISO 8601) | Нет | Начальная дата для фильтрации |
| `end_date` | `datetime` (ISO 8601) | Нет | Конечная дата для фильтрации |

**Example Request:**
```bash
curl http://localhost:8000/api/v1/statistics

# С параметрами дат
curl "http://localhost:8000/api/v1/statistics?start_date=2025-09-01T00:00:00&end_date=2025-10-17T23:59:59"
```

**Response:**
```json
{
  "total_users": 30,
  "active_users": 25,
  "total_messages": 400,
  "avg_messages_per_user": 16.0,
  "messages_by_date": [
    {
      "date": "2025-09-18T00:00:00",
      "count": 15
    },
    {
      "date": "2025-09-19T00:00:00",
      "count": 22
    }
  ],
  "top_users": [
    {
      "user_id": 100000,
      "username": "john_doe",
      "message_count": 45
    },
    {
      "user_id": 100001,
      "username": null,
      "message_count": 38
    }
  ]
}
```

**Response Fields:**

| Поле | Тип | Описание |
|------|-----|----------|
| `total_users` | `integer` | Общее количество пользователей |
| `active_users` | `integer` | Активные пользователи (за последние 30 дней) |
| `total_messages` | `integer` | Общее количество сообщений |
| `avg_messages_per_user` | `float` | Среднее количество сообщений на пользователя |
| `messages_by_date` | `array` | Распределение сообщений по датам |
| `messages_by_date[].date` | `datetime` | Дата |
| `messages_by_date[].count` | `integer` | Количество сообщений за день |
| `top_users` | `array` | Топ-10 активных пользователей |
| `top_users[].user_id` | `integer` | Telegram ID пользователя |
| `top_users[].username` | `string | null` | Telegram username (может быть null) |
| `top_users[].message_count` | `integer` | Количество сообщений пользователя |

**Status codes:**
- `200 OK` - Успешный запрос
- `422 Unprocessable Entity` - Невалидные параметры

---

## Data Models

### StatisticsResponse

```typescript
interface StatisticsResponse {
  total_users: number;          // >= 0
  active_users: number;         // >= 0
  total_messages: number;       // >= 0
  avg_messages_per_user: number; // >= 0
  messages_by_date: MessageByDate[];
  top_users: TopUser[];
}
```

### MessageByDate

```typescript
interface MessageByDate {
  date: string;    // ISO 8601 datetime
  count: number;   // >= 0
}
```

### TopUser

```typescript
interface TopUser {
  user_id: number;        // Telegram ID
  username: string | null; // Telegram username or null
  message_count: number;   // >= 0
}
```

## CORS

API настроен для работы с frontend на следующих origins:
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (React/Next.js)
- `http://127.0.0.1:5173`
- `http://127.0.0.1:3000`

## Error Handling

### Validation Errors (422)

```json
{
  "detail": [
    {
      "loc": ["query", "start_date"],
      "msg": "invalid datetime format",
      "type": "value_error.datetime"
    }
  ]
}
```

## Versioning

API использует URL-based versioning: `/api/v1/...`

Текущая версия: **v1**

## Rate Limiting

Rate limiting не применяется в текущей версии.

## Future Endpoints (Roadmap)

### Chat API

**POST** `/api/v1/chat/message` - отправить сообщение в чат  
**GET** `/api/v1/chat/history/{user_id}` - получить историю чата  
**DELETE** `/api/v1/chat/history/{user_id}` - очистить историю чата

### Admin API

**POST** `/api/v1/admin/query` - Text2SQL запрос (админ режим)

## Testing

### Manual Testing

```bash
# Запуск API
make run-api

# Проверка работоспособности
curl http://localhost:8000/

# Получение статистики
curl http://localhost:8000/api/v1/statistics | jq

# OpenAPI документация
open http://localhost:8000/docs
```

### Automated Testing

```bash
# Запуск всех API тестов
make test-api

# Запуск всех тестов с coverage
make test-cov
```

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Dashboard Requirements](../frontend/dashboard-requirements.md)

