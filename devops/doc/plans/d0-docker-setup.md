# План Спринта D0: Basic Docker Setup

**Статус:** ✅ Завершен  
**Дата:** 2025-10-18

## Цель

Запустить все сервисы проекта (Bot, API, Frontend, PostgreSQL) локально через `docker-compose up` одной командой.

## Архитектура

```
docker-compose.yml
├── postgres       (готово) - PostgreSQL 16
├── migrations     (готово) - Alembic миграции
├── bot            (новый)  - Telegram бот
├── api            (новый)  - FastAPI веб-сервер
└── frontend       (новый)  - React + Vite
```

## Выполненные задачи

### 1. ✅ Создан Dockerfile для Backend (Bot + API)

**Файл:** `Dockerfile.backend`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY prompts ./prompts
COPY alembic ./alembic
COPY alembic.ini ./
RUN uv pip install --system -e .
# Команда будет передана из docker-compose.yml
```

**Особенности:**
- Базовый образ: `python:3.11-slim`
- Использует UV для управления зависимостями
- Копирует только необходимые файлы
- Команда запуска передается из docker-compose.yml

### 2. ✅ Создан Dockerfile для Frontend

**Файл:** `frontend/Dockerfile`

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

**Особенности:**
- Базовый образ: `node:20-alpine` (Vite 7+ требует Node.js 20.19+)
- Запускает dev-сервер Vite с hot-reload
- Доступ из контейнера через `--host 0.0.0.0`

### 3. ✅ Созданы .dockerignore файлы

**Корень проекта:** `.dockerignore`
```
.git
.cursor
.vscode
__pycache__
*.pyc
.pytest_cache
.mypy_cache
.ruff_cache
htmlcov
.coverage
.env
node_modules
frontend/dist
frontend/node_modules
tests
docs
devops
```

**Frontend:** `frontend/.dockerignore`
```
node_modules
dist
.git
coverage
.eslintcache
```

### 4. ✅ Обновлен docker-compose.yml

Добавлены три новых сервиса:

**Bot сервис:**
```yaml
bot:
  build:
    context: .
    dockerfile: Dockerfile.backend
  container_name: systech-aidd-bot
  depends_on:
    migrations:
      condition: service_completed_successfully
  env_file: .env
  environment:
    DATABASE_URL: postgresql+asyncpg://aidd_user:aidd_password@postgres:5432/aidd_db
  command: uv run python -m src.main
  restart: unless-stopped
```

**API сервис:**
```yaml
api:
  build:
    context: .
    dockerfile: Dockerfile.backend
  container_name: systech-aidd-api
  depends_on:
    migrations:
      condition: service_completed_successfully
  env_file: .env
  environment:
    DATABASE_URL: postgresql+asyncpg://aidd_user:aidd_password@postgres:5432/aidd_db
  ports:
    - "8000:8000"
  command: uv run python -m src.api.main
  restart: unless-stopped
```

**Frontend сервис:**
```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  container_name: systech-aidd-frontend
  depends_on:
    - api
  ports:
    - "5173:5173"
  volumes:
    - ./frontend/src:/app/src
  environment:
    VITE_API_BASE_URL: http://localhost:8000/api/v1
  restart: unless-stopped
```

### 5. ✅ Обновлен README.md

Добавлена секция **"🐳 Docker запуск (рекомендуется)"** с:
- Требованиями к системе
- Инструкциями по запуску
- Списком доступа к сервисам
- Полезными командами Docker Compose

## Результаты

### Созданные файлы
1. `Dockerfile.backend` - Docker образ для Bot и API
2. `frontend/Dockerfile` - Docker образ для Frontend
3. `.dockerignore` - исключения для backend
4. `frontend/.dockerignore` - исключения для frontend

### Обновленные файлы
1. `docker-compose.yml` - добавлены сервисы bot, api, frontend
2. `README.md` - добавлена секция Docker запуска

### Архитектура запуска

**Порядок запуска сервисов:**
1. `postgres` - стартует с healthcheck
2. `migrations` - ждет готовности postgres, выполняет миграции
3. `bot` и `api` - стартуют после успешного завершения миграций
4. `frontend` - стартует после запуска API

**Доступ к сервисам:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173
- PostgreSQL: localhost:5433
- Telegram Bot: работает автоматически

## Особенности реализации

### MVP подход
- **Простые Dockerfiles:** однослойные, без multi-stage builds
- **Dev режим:** Frontend с hot-reload через volumes
- **Быстрый старт:** все запускается одной командой
- **Переменные окружения:** из `.env` файла

### Зависимости между сервисами
- Bot и API зависят от успешного завершения миграций
- Frontend зависит от API (но только как hint для compose)
- Postgres имеет healthcheck для надежного старта

### Restart policy
Все сервисы (кроме migrations) используют `restart: unless-stopped` для:
- Автоматического перезапуска при падении
- Сохранения состояния после перезагрузки системы
- Возможности ручной остановки без перезапуска

## Команда запуска

```bash
# Запуск всех сервисов
docker-compose up

# Или в фоновом режиме
docker-compose up -d

# Пересборка образов
docker-compose up --build

# Остановка
docker-compose down

# Полная очистка (включая volumes)
docker-compose down -v
```

## Следующие шаги

Этот спринт создает базу для:
- **D1: Build & Publish** - автоматическая сборка и публикация образов в GitHub Container Registry
- **D2: Развертывание на сервер** - ручное развертывание на production
- **D3: Auto Deploy** - автоматический деплой через GitHub Actions

## Принципы MVP

✅ **Простота** - однослойные Dockerfiles, базовая конфигурация  
✅ **Скорость** - быстрый старт без сложных оптимизаций  
✅ **Функциональность** - все работает одной командой  
✅ **Документация** - понятные инструкции в README  

## Технические детали

### Backend образ
- Размер: ~200MB (python:3.11-slim + зависимости)
- Время сборки: ~1-2 минуты
- Переиспользуется для bot и api

### Frontend образ
- Размер: ~300MB (node:20-alpine + зависимости)
- Время сборки: ~2-3 минуты
- Hot-reload работает через volume mount

## Проблемы при тестировании

### Проблема: Frontend перезапускался из-за ошибки Node.js версии

**Симптомы:**
- Frontend контейнер в статусе `Restarting`
- Ошибка в логах: `You are using Node.js 18.20.8. Vite requires Node.js version 20.19+ or 22.12+`

**Решение:**
- Обновлен Dockerfile: `FROM node:18-alpine` → `FROM node:20-alpine`
- Пересборка: `docker-compose up -d --build frontend`

**Результат:** ✅ Frontend успешно запустился с Vite 7.1.10

### Оптимизации (отложены на будущее)
- Multi-stage builds для уменьшения размера образов
- Layer caching для ускорения сборки
- Production build frontend с nginx
- Health checks для backend сервисов
- Resource limits (CPU, RAM)

