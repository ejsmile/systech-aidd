# 📋 Tasklist SP-3: Frontend с дашбордом и веб-чатом

> **Базовый документ:** [roadmap.md](../roadmap.md)

## 📊 Отчет о прогрессе

| № | Итерация | Статус | Тестирование | Дата завершения |
|---|----------|--------|--------------|-----------------|
| 1.1 | Функциональные требования к дашборду | ✅ Завершено | ✅ Документация | 17.10.2025 |
| 1.2 | Проектирование API контракта | ✅ Завершено | ✅ 10 тестов | 17.10.2025 |
| 1.3 | Проектирование StatCollector интерфейса | ✅ Завершено | ✅ mypy strict | 17.10.2025 |
| 1.4 | Mock реализация StatCollector | ✅ Завершено | ✅ 8 тестов | 17.10.2025 |
| 1.5 | API entrypoint и интеграция | ✅ Завершено | ✅ 9 тестов | 17.10.2025 |
| 2.1 | Frontend концепция и требования | ✅ Завершено | ✅ Документация | 17.10.2025 |
| 2.2 | Выбор технологического стека | ✅ Завершено | ✅ Документация | 17.10.2025 |
| 2.3 | Структура проекта и инструменты | ✅ Завершено | ✅ 3 теста | 17.10.2025 |
| 3.1 | Базовый layout и навигация | ✅ Завершено | ✅ Компоненты + Тесты | 17.10.2025 |
| 3.2 | Реализация дашборда: метрики | ✅ Завершено | ✅ MetricCard + 4 метрики | 17.10.2025 |
| 3.3 | Реализация дашборда: визуализация | ✅ Завершено | ✅ Chart + Table + Skeletons | 17.10.2025 |
| 3.4 | Интеграция с Mock API | ✅ Завершено | ✅ API connection + Auto-refresh | 17.10.2025 |
| 4.1 | API для веб-чата | ✅ Завершено | ✅ Unit + API тесты | 2025-10-17 |
| 4.2 | UI веб-чата | ✅ Завершено | ✅ Chat components | 2025-10-17 |
| 4.3 | Админ-чат: Text2SQL интеграция | ✅ Завершено | ✅ SQL validation + tests | 2025-10-17 |
|| 5.1 | Real StatCollector реализация | ✅ Завершено | ✅ 9 тестов + testcontainers | 2025-10-17 |
|| 5.2 | Интеграция с PostgreSQL | ✅ Завершено | ✅ Async sessions + timezone fix | 2025-10-17 |
|| 5.3 | Переключение Mock → Real | ✅ Завершено | ✅ 151 тестов, coverage 87% | 2025-10-17 |

**Легенда статусов:**
- ⏳ Ожидает
- 🔄 В работе
- ✅ Завершено
- ⚠️ Проблемы

---

## 🎯 Подспринт 1: Mock API для статистики

### 🔍 Итерация 1.1: Функциональные требования к дашборду

**Цель:** Сформировать емкие и лаконичные функциональные требования к дашборду без дополнительных доработок

#### Задачи
- [ ] Проанализировать существующую структуру БД (User, Message)
- [ ] Определить ключевые метрики для отображения
- [ ] Документировать требования в `docs/frontend/dashboard-requirements.md`
- [ ] Создать wireframe/mockup структуры дашборда (текстовое описание)

#### Ключевые метрики (примеры)
- Общее количество пользователей
- Количество активных пользователей (за период)
- Общее количество сообщений
- Среднее количество сообщений на пользователя
- Распределение сообщений по времени
- Топ активных пользователей

#### Результат
- Документ с функциональными требованиями
- Список необходимых метрик
- Понимание структуры данных для API

---

### 🎨 Итерация 1.2: Проектирование API контракта

**Цель:** Спроектировать простой и эффективный API контракт (KISS - один метод для статистики)

#### Задачи
- [ ] Создать `src/api/` директорию
- [ ] Создать `src/api/models.py` с Pydantic моделями для API
- [ ] Спроектировать response model для статистики (StatisticsResponse)
- [ ] Документировать API контракт в `docs/api/api-contract.md`
- [ ] Определить query параметры (опционально: фильтры по дате)

#### Пример структуры API
```python
# GET /api/v1/statistics
StatisticsResponse:
  - total_users: int
  - active_users: int
  - total_messages: int
  - avg_messages_per_user: float
  - messages_by_date: list[MessageByDate]
  - top_users: list[TopUser]
```

#### Тест
- Валидация Pydantic моделей
- Проверка соответствия требованиям из 1.1

---

### 🏗️ Итерация 1.3: Проектирование StatCollector интерфейса

**Цель:** Создать абстракцию для сбора статистики с поддержкой Mock и Real реализаций

#### Задачи
- [ ] Создать `src/api/stat_collector.py`
- [ ] Определить абстрактный класс/Protocol `StatCollectorProtocol`
- [ ] Определить методы интерфейса (например, `get_statistics()`)
- [ ] Добавить type hints для всех методов
- [ ] Написать docstrings с описанием контракта

#### Структура
```python
class StatCollectorProtocol(Protocol):
    async def get_statistics(
        self, 
        start_date: datetime | None = None,
        end_date: datetime | None = None
    ) -> StatisticsResponse:
        """Получить статистику по диалогам."""
        ...
```

#### Тест
- Проверка что протокол корректно определен
- mypy проверка типов

---

### 🎭 Итерация 1.4: Mock реализация StatCollector

**Цель:** Реализовать Mock версию сборщика статистики с фейковыми данными

#### Задачи
- [ ] Создать `src/api/mock_stat_collector.py`
- [ ] Реализовать класс `MockStatCollector`
- [ ] Сгенерировать реалистичные фейковые данные
- [ ] Добавить возможность настройки объема mock данных
- [ ] Написать unit-тесты для MockStatCollector
- [ ] Добавить docstrings и type hints

#### Mock данные
- 10-50 "пользователей"
- 100-500 "сообщений"
- Распределение по последним 30 дням
- Реалистичные соотношения метрик

#### Тест
```bash
# Автоматизированное тестирование
make test  # Проверка MockStatCollector

# Ручная проверка
python -m pytest tests/test_mock_stat_collector.py -v
```

---

### 🚀 Итерация 1.5: API entrypoint и интеграция

**Цель:** Создать FastAPI приложение с endpoint для статистики

#### Задачи
- [ ] Добавить FastAPI в зависимости (`pyproject.toml`)
- [ ] Создать `src/api/app.py` с FastAPI приложением
- [ ] Реализовать endpoint `GET /api/v1/statistics`
- [ ] Добавить CORS middleware для frontend
- [ ] Настроить автоматическую документацию (OpenAPI/Swagger)
- [ ] Создать `src/api/main.py` для запуска API
- [ ] Добавить команды в Makefile: `make run-api`, `make test-api`
- [ ] Написать интеграционные тесты для API endpoint

#### Зависимости
```toml
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
```

#### Тест
```bash
# Запуск API
make run-api
# Должен запуститься на http://localhost:8000

# Проверка endpoint
curl http://localhost:8000/api/v1/statistics

# Проверка документации
# Открыть http://localhost:8000/docs

# Автоматизированное тестирование
make test-api
```

---

## 🎨 Подспринт 2: Каркас frontend проекта

### 📝 Итерация 2.1: Frontend концепция и требования

**Цель:** Определить видение и требования к frontend приложению

#### Задачи
- [ ] Создать директорию `frontend/docs/`
- [ ] Создать `frontend/docs/front-vision.md` (по аналогии с vision.md)
- [ ] Определить целевую аудиторию (администраторы системы)
- [ ] Описать основные экраны (Dashboard, Chat, Settings)
- [ ] Определить требования к UX/UI (modern, clean, responsive)
- [ ] Описать принципы дизайна и архитектуры

#### Содержание front-vision.md
- Целевая аудитория
- Основные функции
- Навигация между экранами
- Требования к дизайну
- Требования к производительности
- Требования к доступности

---

### 🔧 Итерация 2.2: Выбор технологического стека

**Цель:** Выбрать оптимальный набор frontend технологий

#### Задачи
- [ ] Исследовать современные frontend фреймворки
- [ ] Выбрать основной фреймворк (React/Vue/Svelte)
- [ ] Выбрать библиотеку для UI компонентов
- [ ] Выбрать библиотеку для графиков/визуализации
- [ ] Выбрать инструменты для state management
- [ ] Выбрать HTTP клиент для API
- [ ] Документировать решения в `frontend/docs/tech-stack.md`

#### Рекомендуемый стек (KISS принцип)
- **Фреймворк:** React 18+ с TypeScript
- **UI библиотека:** Shadcn/ui или Chakra UI
- **Графики:** Recharts или Chart.js
- **State:** React Context API (избегаем Redux)
- **HTTP:** fetch API или axios
- **Build:** Vite
- **Тестирование:** Vitest + React Testing Library

#### Критерии выбора
- Простота использования
- Качество документации
- Размер bundle
- TypeScript поддержка
- Активность сообщества

---

### 🏗️ Итерация 2.3: Структура проекта и инструменты

**Цель:** Создать структуру frontend проекта и настроить инструменты разработки

#### Задачи
- [ ] Создать `frontend/` директорию
- [ ] Инициализировать проект (vite create или аналог)
- [ ] Настроить TypeScript конфигурацию
- [ ] Настроить ESLint + Prettier
- [ ] Создать структуру директорий
- [ ] Настроить package.json скрипты
- [ ] Создать базовый App компонент
- [ ] Добавить команды в Makefile: `make frontend-dev`, `make frontend-build`

#### Структура директорий
```
frontend/
├── docs/              # Документация
├── src/
│   ├── components/    # Переиспользуемые компоненты
│   ├── pages/         # Страницы (Dashboard, Chat)
│   ├── api/           # API клиент
│   ├── types/         # TypeScript типы
│   ├── hooks/         # Custom hooks
│   ├── utils/         # Утилиты
│   ├── App.tsx
│   └── main.tsx
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .eslintrc.js
```

#### Тест
```bash
# Установка зависимостей
cd frontend && npm install

# Запуск dev сервера
make frontend-dev
# Должен запуститься на http://localhost:5173

# Сборка для продакшена
make frontend-build

# Проверка качества кода
cd frontend && npm run lint
```

---

## 📊 Подспринт 3: Реализация Dashboard

### 🎨 Итерация 3.1: Базовый layout и навигация

**Цель:** Создать основной layout приложения с навигацией

#### Задачи
- [ ] Создать `src/components/Layout.tsx`
- [ ] Реализовать sidebar с навигацией
- [ ] Создать header с заголовком
- [ ] Настроить routing (React Router)
- [ ] Создать заглушки страниц (Dashboard, Chat)
- [ ] Добавить responsive дизайн
- [ ] Написать тесты для Layout компонента

#### Компоненты
- `Layout.tsx` - главный layout
- `Sidebar.tsx` - боковая панель навигации
- `Header.tsx` - верхняя панель

#### Тест
```bash
# Визуальная проверка
make frontend-dev
# Проверить навигацию между Dashboard и Chat
# Проверить responsive на разных размерах экрана

# Автоматизированные тесты
cd frontend && npm test
```

---

### 📈 Итерация 3.2: Реализация дашборда - метрики

**Цель:** Отобразить основные метрики в виде карточек

#### Задачи
- [ ] Создать `src/pages/Dashboard.tsx`
- [ ] Создать `src/components/MetricCard.tsx`
- [ ] Реализовать grid layout для карточек
- [ ] Отобразить ключевые метрики (total users, messages, etc.)
- [ ] Добавить loading состояния
- [ ] Добавить error обработку
- [ ] Написать тесты для Dashboard и MetricCard

#### Метрики для отображения
- Всего пользователей
- Активных пользователей
- Всего сообщений
- Среднее сообщений на пользователя

#### Тест
```bash
# Визуальная проверка
make frontend-dev
# Проверить отображение всех метрик
# Проверить loading состояние
# Проверить responsive layout
```

---

### 📊 Итерация 3.3: Реализация дашборда - визуализация

**Цель:** Добавить графики и визуализацию данных

#### Задачи
- [ ] Установить библиотеку для графиков
- [ ] Создать `src/components/MessagesByDateChart.tsx`
- [ ] Создать `src/components/TopUsersTable.tsx`
- [ ] Реализовать график сообщений по дням
- [ ] Реализовать таблицу топ пользователей
- [ ] Добавить легенду и tooltips
- [ ] Написать тесты для компонентов графиков

#### Визуализации
- Line/Bar chart: сообщения по дням
- Table: топ 10 активных пользователей

#### Тест
```bash
# Визуальная проверка
make frontend-dev
# Проверить отображение графиков
# Проверить интерактивность (hover, tooltips)
# Проверить корректность данных
```

---

### 🔌 Итерация 3.4: Интеграция с Mock API

**Цель:** Подключить frontend к Mock API для получения реальных данных

#### Задачи
- [ ] Создать `src/api/client.ts` - HTTP клиент
- [ ] Создать `src/api/statistics.ts` - методы для статистики
- [ ] Создать `src/types/statistics.ts` - TypeScript типы
- [ ] Интегрировать API вызов в Dashboard
- [ ] Добавить loading индикаторы
- [ ] Добавить error handling и retry логику
- [ ] Добавить auto-refresh (опционально)
- [ ] Написать интеграционные тесты

#### API Client
```typescript
// src/api/client.ts
const API_BASE_URL = 'http://localhost:8000/api/v1';

export async function getStatistics() {
  const response = await fetch(`${API_BASE_URL}/statistics`);
  return response.json();
}
```

#### Тест
```bash
# Запустить API
make run-api

# Запустить frontend
make frontend-dev

# Проверить что данные загружаются с API
# Проверить Network tab в DevTools
# Проверить обработку ошибок (остановить API)
```

---

## 💬 Подспринт 4: Реализация ИИ-чата

### 🔧 Итерация 4.1: API для веб-чата

**Цель:** Создать API endpoints для веб-чата (аналог Telegram бота)

#### Задачи
- [ ] Расширить `src/api/models.py` моделями для чата
- [ ] Создать `src/api/chat_handler.py`
- [ ] Реализовать endpoint `POST /api/v1/chat/message`
- [ ] Реализовать endpoint `GET /api/v1/chat/history/{user_id}`
- [ ] Реализовать endpoint `DELETE /api/v1/chat/history/{user_id}`
- [ ] Интегрировать с существующим LLMClient
- [ ] Интегрировать с ConversationManager
- [ ] Добавить поддержку streaming ответов (SSE - опционально)
- [ ] Написать тесты для chat endpoints

#### API Endpoints
```python
POST /api/v1/chat/message
  Request: { user_id: str, message: str }
  Response: { response: str, message_id: int }

GET /api/v1/chat/history/{user_id}
  Response: { messages: list[Message] }

DELETE /api/v1/chat/history/{user_id}
  Response: { success: bool }
```

#### Тест
```bash
# Автоматизированное тестирование
make test-api

# Ручное тестирование
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"user_id": "web-user-1", "message": "Привет!"}'
```

---

### 💬 Итерация 4.2: UI веб-чата

**Цель:** Создать интерфейс веб-чата для общения с ботом

#### Задачи
- [ ] Создать `src/pages/Chat.tsx`
- [ ] Создать `src/components/ChatMessage.tsx`
- [ ] Создать `src/components/ChatInput.tsx`
- [ ] Реализовать отображение истории сообщений
- [ ] Реализовать ввод и отправку сообщений
- [ ] Добавить auto-scroll к новым сообщениям
- [ ] Добавить typing indicator
- [ ] Добавить кнопку очистки истории
- [ ] Написать тесты для chat компонентов

#### UI Features
- Список сообщений (user/assistant)
- Input для ввода сообщения
- Кнопка отправки
- Loading indicator при ожидании ответа
- Кнопка "Clear history"

#### Тест
```bash
# Запустить API и frontend
make run-api
make frontend-dev

# Проверить отправку сообщений
# Проверить получение ответов
# Проверить очистку истории
# Проверить responsive дизайн
```

---

### 🧠 Итерация 4.3: Админ-чат с Text2SQL

**Цель:** Реализовать специальный режим чата для администратора с Text2SQL

#### Задачи
- [ ] Создать `src/api/text2sql_handler.py`
- [ ] Реализовать Text2SQL промпт для LLM
- [ ] Реализовать выполнение SQL запросов (read-only)
- [ ] Добавить безопасность (whitelist таблиц, запрет на DELETE/UPDATE)
- [ ] Реализовать endpoint `POST /api/v1/admin/query`
- [ ] Добавить UI toggle для админ режима в Chat
- [ ] Добавить отображение SQL запроса и результатов
- [ ] Написать тесты для Text2SQL функционала

#### Text2SQL Flow
1. Пользователь: "Сколько сообщений отправил пользователь с ID 123?"
2. LLM генерирует SQL: `SELECT COUNT(*) FROM messages WHERE user_id = 123`
3. Система выполняет SQL
4. Результат возвращается в LLM
5. LLM формулирует ответ: "Пользователь отправил 42 сообщения"

#### Безопасность
- Read-only доступ к БД
- Whitelist таблиц (только messages, users)
- Валидация SQL запросов
- Rate limiting

#### Тест
```bash
# Тестирование через UI
make run-api
make frontend-dev

# Включить админ режим в Chat
# Задать вопрос: "Сколько всего пользователей?"
# Проверить что показывается SQL запрос
# Проверить корректность ответа
```

---

## 🔄 Подспринт 5: Переход на Real API

### 💾 Итерация 5.1: Real StatCollector реализация

**Цель:** Реализовать настоящий сборщик статистики на основе PostgreSQL

#### Задачи
- [x] Создать `src/api/real_stat_collector.py`
- [x] Реализовать класс `RealStatCollector`
- [x] Реализовать SQL запросы для всех метрик
- [x] Оптимизировать запросы (использовать JOIN, агрегации)
- [ ] ~~Добавить кэширование результатов~~ (отложено - данных пока немного)
- [x] Написать unit-тесты с testcontainers (9 тестов)
- [x] Добавить тест для timezone-aware datetime

#### SQL Queries Examples
```sql
-- Total users
SELECT COUNT(*) FROM users;

-- Active users (last 30 days)
SELECT COUNT(DISTINCT user_id) 
FROM messages 
WHERE created_at > NOW() - INTERVAL '30 days';

-- Messages by date
SELECT DATE(created_at), COUNT(*) 
FROM messages 
GROUP BY DATE(created_at) 
ORDER BY DATE(created_at);
```

#### Тест
```bash
# Автоматизированное тестирование
make test

# Проверить что RealStatCollector работает с реальной БД
# Проверить корректность метрик
# Замерить производительность
```

---

### 🔗 Итерация 5.2: Интеграция с PostgreSQL

**Цель:** Подключить RealStatCollector к существующей PostgreSQL

#### Задачи
- [x] Добавить конфигурацию для выбора collector типа
- [x] Интегрировать RealStatCollector с database session
- [x] Настроить connection pooling для API
- [x] Добавить error handling для DB ошибок
- [x] Написать интеграционные тесты
- [x] Добавить функцию `_to_naive_datetime()` для timezone конвертации
- [x] Обновить документацию API

#### Configuration
```python
# src/api/config.py
class APIConfig(BaseSettings):
    use_mock_data: bool = False  # False = use Real collector
    database_url: str
    # ... другие настройки
```

#### Тест
```bash
# Запустить с реальной БД
USE_MOCK_DATA=false make run-api

# Проверить что данные загружаются из PostgreSQL
# Проверить через frontend что статистика реальная
```

---

### 🎯 Итерация 5.3: Переключение Mock → Real

**Цель:** Финальное переключение на реальную реализацию

#### Задачи
- [x] Создать factory для выбора StatCollector (прямая интеграция в app.py)
- [x] Обновить API app для использования RealStatCollector
- [x] Исправить main.py для экспорта app
- [x] Протестировать Real режим
- [x] Перевести все API тесты на async httpx.AsyncClient
- [x] Обновить README с инструкциями
- [x] Финальное тестирование всего функционала (151/151 тестов)

#### Factory Pattern
```python
# src/api/factory.py
def create_stat_collector(config: APIConfig) -> StatCollectorProtocol:
    if config.use_mock_data:
        return MockStatCollector()
    else:
        return RealStatCollector(session_factory)
```

#### Тест
```bash
# Полный цикл тестирования

# 1. Mock режим
USE_MOCK_DATA=true make run-api
make frontend-dev
# Проверить что все работает с mock данными

# 2. Real режим
USE_MOCK_DATA=false make run-api
make frontend-dev
# Проверить что все работает с реальной БД

# 3. Проверить Dashboard
# - Все метрики отображаются
# - Графики работают
# - Данные актуальные

# 4. Проверить Chat
# - Отправка сообщений
# - Получение ответов
# - Очистка истории
# - Админ режим (Text2SQL)

# 5. Проверить качество кода
make quality
make test-cov  # Coverage > 70%
```

---

## 📝 Финальная проверка

### Чеклист готовности

#### Backend (API)
- [ ] FastAPI работает корректно
- [ ] Все endpoints документированы (OpenAPI)
- [ ] Mock и Real режимы работают
- [ ] Тесты покрывают > 70% кода
- [ ] CORS настроен для frontend
- [ ] Error handling везде

#### Frontend
- [ ] Dashboard отображает все метрики
- [ ] Графики работают корректно
- [ ] Chat функционирует полностью
- [ ] Админ режим (Text2SQL) работает
- [ ] Responsive дизайн на всех экранах
- [ ] Loading/Error states везде
- [ ] TypeScript без ошибок
- [ ] Lint проверки проходят

#### Интеграция
- [ ] Frontend успешно взаимодействует с API
- [ ] Real данные из PostgreSQL отображаются
- [ ] Нет CORS ошибок
- [ ] Performance приемлемый

#### Документация
- [ ] `docs/frontend/front-vision.md` создан
- [ ] `docs/frontend/dashboard-requirements.md` создан
- [ ] `docs/frontend/tech-stack.md` создан
- [ ] `docs/api/api-contract.md` создан
- [ ] README обновлен с инструкциями

#### Команды
- [ ] `make run-api` - запуск API
- [ ] `make test-api` - тестирование API
- [ ] `make frontend-dev` - запуск frontend dev
- [ ] `make frontend-build` - сборка frontend
- [ ] `make quality` - проверка качества
- [ ] `make test-cov` - тесты с coverage

---

## 📚 Дополнительные материалы

### Рекомендуемые референсы для UI

#### Dashboard
- [Vercel Analytics Dashboard](https://vercel.com/analytics)
- [Plausible Analytics](https://plausible.io)
- [Grafana](https://grafana.com)

#### Chat UI
- [OpenAI ChatGPT](https://chat.openai.com)
- [Claude UI](https://claude.ai)
- [Telegram Web](https://web.telegram.org)

### Полезные библиотеки

#### Backend
- `fastapi` - web framework
- `uvicorn`