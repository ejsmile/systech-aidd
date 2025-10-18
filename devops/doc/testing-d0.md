# Инструкция по тестированию D0: Basic Docker Setup

## Предварительные требования

1. Установлен Docker и Docker Compose
2. Есть файл `.env` с корректными токенами (скопирован из `sample.env`)

## Шаги проверки

### 1. Проверка конфигурации

```bash
# Валидация docker-compose.yml
docker-compose config --quiet

# Если команда выполнена без ошибок - конфигурация валидна ✅
```

### 2. Запуск всех сервисов

```bash
# Запуск в фоновом режиме
docker-compose up -d

# Или с просмотром логов
docker-compose up
```

**Ожидаемый результат:**
- Postgres запускается и проходит healthcheck
- Migrations выполняются успешно
- Bot и API запускаются и подключаются к БД
- Frontend запускается и компилируется

### 3. Проверка статуса сервисов

```bash
# Проверить статус всех контейнеров
docker-compose ps

# Ожидаемый вывод:
# systech-aidd-bot       Up
# systech-aidd-api       Up (0.0.0.0:8000->8000/tcp)
# systech-aidd-frontend  Up (0.0.0.0:5173->5173/tcp)
# systech-aidd-postgres  Up (healthy) (0.0.0.0:5433->5432/tcp)
```

### 4. Проверка API

```bash
# Проверить health endpoint (если есть)
curl http://localhost:8000/docs

# Или открыть в браузере:
# http://localhost:8000/docs - должна открыться Swagger документация ✅
```

### 5. Проверка Frontend

```bash
# Открыть в браузере:
# http://localhost:5173 - должен открыться frontend ✅
```

### 6. Проверка логов

```bash
# Посмотреть логи всех сервисов
docker-compose logs

# Посмотреть логи конкретного сервиса
docker-compose logs bot
docker-compose logs api
docker-compose logs frontend

# Следить за логами в реальном времени
docker-compose logs -f
```

**Что проверить в логах:**
- ✅ Postgres: `database system is ready to accept connections`
- ✅ Migrations: `Running upgrade ... -> ..., OK`
- ✅ Bot: подключение к Telegram, нет ошибок
- ✅ API: `Application startup complete` на порту 8000
- ✅ Frontend: `VITE ... ready in ... ms` и `Local: http://0.0.0.0:5173/`

### 7. Проверка Telegram Bot

```bash
# Отправить команду /start боту в Telegram
# Бот должен ответить ✅
```

### 8. Проверка Frontend → API взаимодействия

```bash
# В Frontend попробовать отправить сообщение в чат
# Запрос должен пройти в API и вернуть ответ ✅
```

## Остановка и очистка

```bash
# Остановить все сервисы
docker-compose down

# Остановить и удалить volumes (полная очистка)
docker-compose down -v
```

## Возможные проблемы

### Проблема: Порты уже заняты

```bash
# Проверить, какие процессы используют порты
lsof -i :5432  # Postgres
lsof -i :8000  # API
lsof -i :5173  # Frontend

# Решение: остановить процессы или изменить порты в docker-compose.yml
```

### Проблема: Ошибка подключения к БД

```bash
# Проверить, что Postgres запущен и healthy
docker-compose ps postgres

# Проверить логи Postgres
docker-compose logs postgres

# Решение: подождать, пока Postgres пройдет healthcheck
```

### Проблема: Frontend не может подключиться к API

```bash
# Проверить переменную окружения
docker-compose exec frontend env | grep VITE_API_BASE_URL

# Должно быть: VITE_API_BASE_URL=http://localhost:8000/api/v1

# Если неверно - обновить docker-compose.yml и пересоздать контейнер
docker-compose up -d --force-recreate frontend
```

### Проблема: Bot не отвечает в Telegram

```bash
# Проверить логи бота
docker-compose logs bot

# Проверить токен в .env файле
# TELEGRAM_TOKEN должен быть корректным

# Решение: обновить .env и перезапустить
docker-compose restart bot
```

## Checklist готовности

- [ ] `docker-compose config --quiet` - без ошибок
- [ ] `docker-compose up` - все сервисы запускаются
- [ ] `docker-compose ps` - все контейнеры в статусе Up
- [ ] http://localhost:8000/docs - открывается Swagger
- [ ] http://localhost:5173 - открывается frontend
- [ ] Bot отвечает на команду /start в Telegram
- [ ] Frontend может отправлять запросы в API

## Результат

✅ Спринт D0 считается завершенным, если все пункты checklist выполнены.

Команда `docker-compose up` успешно запускает весь проект!

