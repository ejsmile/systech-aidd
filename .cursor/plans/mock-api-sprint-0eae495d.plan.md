<!-- 0eae495d-1f83-4984-b227-1ba3b03344b0 af2a05d9-9982-48d0-ac0d-897fdb7ffc20 -->
# Mock API для статистики - Подспринт 1

## Обзор

Реализация Mock API для дашборда статистики, которое позже будет заменено на реальные запросы к PostgreSQL. Следует принципам KISS проекта и использует существующие паттерны из кодовой базы бота.

## Шаги реализации

### 1. Документация требований к дашборду

**Цель:** Определить четкие метрики на основе существующей схемы БД (таблицы User, Message)

**Файлы для создания:**

- `docs/frontend/dashboard-requirements.md` - документ с функциональными требованиями

**Ключевые метрики для определения:**

- Общее количество пользователей
- Активные пользователи (с сообщениями за последние 30 дней)
- Общее количество сообщений
- Среднее количество сообщений на пользователя
- Распределение сообщений по датам (последние 30 дней)
- Топ-10 активных пользователей

**Проверка:** Документ гарантирует, что все метрики соответствуют доступным полям БД (user_id, created_at, chat_id и т.д.)

---

### 2. Проектирование API контракта

**Цель:** Спроектировать Pydantic модели для ответов API статистики

**Файлы для создания:**

- `src/api/models.py` - Pydantic модели ответов по паттерну существующего config.py

**Модели для реализации:**

```python
class MessageByDate(BaseModel):
    date: datetime
    count: int

class TopUser(BaseModel):
    user_id: int
    username: str | None
    message_count: int

class StatisticsResponse(BaseModel):
    total_users: int
    active_users: int
    total_messages: int
    avg_messages_per_user: float
    messages_by_date: list[MessageByDate]
    top_users: list[TopUser]
```

**Тест:** Создать `tests/test_api_models.py` для валидации Pydantic моделей

---

### 3. Протокол StatCollector

**Цель:** Определить интерфейс для сбора статистики (Mock и Real реализации)

**Файлы для создания:**

- `src/api/stat_collector.py` - определение Protocol с type hints

**Структура протокола:**

```python
from typing import Protocol
from datetime import datetime

class StatCollectorProtocol(Protocol):
    async def get_statistics(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> StatisticsResponse:
        """Получить статистику по диалогам."""
        ...
```

**Проверка:** Выполнить `make typecheck` чтобы убедиться что mypy принимает протокол

---

### 4. Реализация Mock StatCollector

**Цель:** Реализовать mock версию с реалистичными фейковыми данными

**Файлы для создания:**

- `src/api/mock_stat_collector.py` - класс MockStatCollector
- `tests/test_mock_stat_collector.py` - unit тесты

**Генерация mock данных:**

- 20-50 фейковых пользователей с реалистичными username
- 200-500 фейковых сообщений, распределенных по последним 30 дням
- Реалистичные соотношения (некоторые пользователи активнее других)
- Использовать модули `datetime` и `random` для генерации данных

**Паттерн:** Следовать существующему паттерну repository из `src/repository.py`

**Команда теста:** `make test` должен пройти все тесты MockStatCollector

---

### 5. Интеграция FastAPI

**Цель:** Создать FastAPI приложение с endpoint для статистики

**Зависимости для добавления в pyproject.toml:**

```toml
"fastapi>=0.104.0",
"uvicorn[standard]>=0.24.0",
```

**Файлы для создания:**

- `src/api/app.py` - FastAPI приложение с CORS
- `src/api/main.py` - точка входа для запуска API
- `docs/api/api-contract.md` - документация API
- `tests/test_api_endpoints.py` - интеграционные тесты

**Endpoint:**

```python
GET /api/v1/statistics
Query параметры: start_date?, end_date? (ISO формат)
Response: модель StatisticsResponse
```

**Дополнения в Makefile:**

```makefile
run-api:
    uv run python -m src.api.main

test-api:
    uv run pytest tests/test_api_endpoints.py -v
```

**Настройка CORS:** Разрешить localhost:5173 (Vite по умолчанию) и localhost:3000

**Проверка тестами:**

- `make run-api` запускает сервер на http://localhost:8000
- `curl http://localhost:8000/api/v1/statistics` возвращает JSON
- OpenAPI документация доступна на http://localhost:8000/docs
- `make test-api` проходит интеграционные тесты
- `make quality` проходит все проверки

---

## Ключевые принципы

1. **KISS:** Простая, понятная реализация без избыточного проектирования
2. **Type Safety:** Полные type hints на всех функциях/методах (mypy strict mode)
3. **Async:** Все методы используют async/await (согласованность с паттернами aiogram)
4. **Testing:** Unit тесты для моделей/mock, интеграционные тесты для API
5. **Documentation:** Четкие docstrings, авто-документация API через FastAPI

## Структура файлов

```
src/api/
├── __init__.py
├── models.py           # Pydantic модели
├── stat_collector.py   # Определение Protocol
├── mock_stat_collector.py  # Mock реализация
├── app.py              # FastAPI приложение
└── main.py             # Точка входа

docs/
├── frontend/
│   └── dashboard-requirements.md
└── api/
    └── api-contract.md

tests/
├── test_api_models.py
├── test_mock_stat_collector.py
└── test_api_endpoints.py
```

## Критерии успеха

- Все проверки типов проходят (mypy strict mode)
- Покрытие тестами > 70% для нового API кода
- API отдает реалистичные mock данные
- OpenAPI документация полная
- Все проверки качества проходят: `make quality`

### To-dos

- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled
- [ ] Duplicate - cancelled