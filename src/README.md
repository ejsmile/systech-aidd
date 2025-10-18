# Backend API README

Краткий обзор API и как его запустить. Подробные контракты см. в `docs/api/api-contract.md`.

## Запуск API локально
```bash
# Предусловия: Python 3.11+, uv, Docker; .env заполнен (DATABASE_URL, OPENROUTER_API_KEY, TELEGRAM_TOKEN)
uv venv
uv pip install -e ".[dev]"
make db-up && make db-migrate
make run-api    # запустит FastAPI на http://localhost:8000
```

## Базовый URL
```
http://localhost:8000/api/v1
```

## Endpoints

### Statistics
- GET `/statistics`
  - query: `start_date`, `end_date` (ISO8601)
  - ответ: агрегированные метрики, распределения, топ пользователей

### Chat
- POST `/chat/message`
  - body: `{ "user_id": string, "message": string }`
  - ответ: `{ "reply": string }`

- GET `/chat/history/{user_id}`
  - ответ: список сообщений (role, content, created_at)

- DELETE `/chat/history/{user_id}`
  - действие: soft delete истории диалога

### Admin (Text2SQL)
- POST `/admin/query`
  - body: `{ "query": string }`
  - ответ: `{ "columns": string[], "rows": any[][] }` или сообщение об ошибке

## Конфигурация (минимум)
```bash
DATABASE_URL=postgresql+asyncpg://aidd_user:aidd_password@localhost:5433/aidd_db
OPENROUTER_API_KEY=...
TELEGRAM_TOKEN=...
LOG_LEVEL=INFO
```

## Заметки
- Источник правды для параметров PostgreSQL — `docker-compose.yml`.
- Для миграций используйте `make db-migrate` или `docker compose run --rm migrations`.
- Доп. детали FastAPI приложения: `src/api/app.py`, `src/api/models.py`.

