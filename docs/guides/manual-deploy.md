# 🚀 Руководство по развертыванию на Production сервер

> **Спринт D2:** Ручное развертывание приложения на удаленном сервере

## 📋 Обзор

Это пошаговая инструкция для развертывания приложения Systech AIDD на production сервере `83.147.246.172` с использованием Docker образов из GitHub Container Registry.

### Параметры сервера
- **Адрес:** 83.147.246.172
- **Пользователь:** systech
- **SSH ключ:** предоставлен отдельно
- **Рабочая директория:** /opt/systech/pkarasov
- **Порты:** 3001 (Frontend), 8001 (API)
- **Docker и Docker Compose:** установлены

### Образы Docker
- `ghcr.io/ejsmile/systech-aidd-bot:latest`
- `ghcr.io/ejsmile/systech-aidd-api:latest`
- `ghcr.io/ejsmile/systech-aidd-frontend:latest`

---

## 🔧 Подготовка локально

### 1. Проверка SSH ключа

Убедитесь, что у вас есть SSH ключ для доступа к серверу:

```bash
# Проверка наличия SSH ключа
ls -la ~/.ssh/

# Тест подключения к серверу
ssh -i ~/.ssh/your_key systech@83.147.246.172 "echo 'SSH connection successful'"
```

### 2. Подготовка файлов для копирования

Подготовьте следующие файлы:

```bash
# Создайте рабочую директорию
mkdir -p ~/systech-deploy
cd ~/systech-deploy

# Скопируйте файлы из проекта
cp /path/to/systech-aidd-my/docker-compose.prod.yml .
cp /path/to/systech-aidd-my/env.production .
cp /path/to/systech-aidd-my/prompts/system.txt .

# Примечание: файлы миграций (alembic/) встроены в Docker образ
# и не требуют отдельного копирования
```

### 3. Настройка переменных окружения

Отредактируйте файл `env.production` и заполните реальными значениями:

```bash
# Откройте файл для редактирования
nano env.production

# Заполните обязательные переменные:
# - TELEGRAM_TOKEN=ваш_токен_бота
# - OPENROUTER_API_KEY=ваш_api_ключ
# - POSTGRES_PASSWORD=сложный_пароль
# - CORS_ORIGINS (уже настроен для production сервера)
```

**Важно:** Используйте сильный пароль для PostgreSQL (минимум 16 символов).

**CORS настройки:** Переменная `CORS_ORIGINS` уже настроена для работы с production сервером. Она включает:
- localhost порты для разработки
- production сервер: `http://83.147.246.172:3001`

### 4. Проверка доступа к серверу

```bash
# Проверка доступности сервера
ping 83.147.246.172

# Проверка SSH доступа
ssh -i ~/.ssh/your_key systech@83.147.246.172 "docker --version && docker compose version"
```

---

## 🖥️ Подключение к серверу

### 1. SSH подключение

```bash
# Подключение к серверу
ssh -i ~/.ssh/your_key systech@83.147.246.172
```

### 2. Проверка окружения

```bash
# Проверка версий Docker
docker --version
docker compose version

# Проверка доступного места на диске
df -h

# Проверка доступной памяти
free -h

# Проверка загруженности CPU
top -bn1 | head -20
```

### 3. Создание рабочей директории

```bash
# Создание директории проекта
sudo mkdir -p /opt/systech/pkarasov
sudo chown systech:systech /opt/systech/pkarasov
cd /opt/systech/pkarasov

# Создание поддиректорий
mkdir -p prompts
```

---

## 📁 Копирование файлов на сервер

### 1. Копирование через SCP

В **новом терминале** (не закрывая SSH сессию):

```bash
# Копирование docker-compose.prod.yml
scp -i ~/.ssh/your_key docker-compose.prod.yml systech@83.147.246.172:/opt/systech/pkarasov/

# Копирование env.production
scp -i ~/.ssh/your_key env.production systech@83.147.246.172:/opt/systech/pkarasov/

# Копирование промпта
scp -i ~/.ssh/your_key system.txt systech@83.147.246.172:/opt/systech/pkarasov/prompts/

# Примечание: файлы миграций (alembic/) встроены в Docker образ
# и автоматически доступны в контейнере
```

### 2. Проверка скопированных файлов

В SSH сессии на сервере:

```bash
# Проверка наличия файлов
ls -la /opt/systech/pkarasov/
ls -la /opt/systech/pkarasov/prompts/

# Проверка содержимого docker-compose.prod.yml
head -20 docker-compose.prod.yml

# Создать .env файл с именем проекта для удобства
echo "COMPOSE_PROJECT_NAME=systech-aidd" > .env
```

---

## ⚙️ Настройка окружения

### 1. Создание .env файла

```bash
# Переименование env.production в .env
mv env.production .env

# Проверка прав доступа
chmod 600 .env
ls -la .env

# Примечание: .env файл с COMPOSE_PROJECT_NAME уже создан выше
```

### 2. Проверка конфигурации

```bash
# Проверка синтаксиса docker-compose
docker compose -f docker-compose.prod.yml config

# Проверка переменных окружения
grep -v "^#" .env | grep -v "^$"
```

---

## 🔐 Авторизация в GitHub Container Registry

### 1. Проверка доступа к образам

```bash
# Попытка загрузки образов (если они публичные)
docker pull ghcr.io/ejsmile/systech-aidd-bot:latest
docker pull ghcr.io/ejsmile/systech-aidd-api:latest
docker pull ghcr.io/ejsmile/systech-aidd-frontend:latest
```

### 2. Авторизация (если образы приватные)

```bash
# Login в GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# Или с паролем
docker login ghcr.io
# Username: your_github_username
# Password: your_github_token
```

---

## 🚀 Загрузка и запуск сервисов

### 1. Загрузка образов

```bash
# Загрузка всех образов
docker compose -f docker-compose.prod.yml pull

# Проверка загруженных образов
docker images | grep systech-aidd
```

### 2. Запуск сервисов

```bash
# Запуск всех сервисов в фоновом режиме
docker compose -f docker-compose.prod.yml up -d

# Проверка статуса контейнеров
docker compose -f docker-compose.prod.yml ps
```

### 3. Мониторинг запуска

```bash
# Просмотр логов всех сервисов
docker compose -f docker-compose.prod.yml logs -f

# Просмотр логов конкретного сервиса
docker compose -f docker-compose.prod.yml logs -f postgres
docker compose -f docker-compose.prod.yml logs -f migrations
docker compose -f docker-compose.prod.yml logs -f bot
docker compose -f docker-compose.prod.yml logs -f api
docker compose -f docker-compose.prod.yml logs -f frontend
```

---

## ✅ Проверка работоспособности

### 1. Проверка статуса контейнеров

```bash
# Статус всех контейнеров
docker compose -f docker-compose.prod.yml ps

# Детальная информация
docker compose -f docker-compose.prod.yml ps -a
```

**Ожидаемый результат:**
```
NAME                     IMAGE                                          STATUS
systech-aidd-postgres    postgres:16-alpine                            Up (healthy)
systech-aidd-bot         ghcr.io/ejsmile/systech-aidd-bot:latest       Up
systech-aidd-api         ghcr.io/ejsmile/systech-aidd-api:latest       Up
systech-aidd-frontend    ghcr.io/ejsmile/systech-aidd-frontend:latest  Up
```

### 2. Проверка healthcheck PostgreSQL

```bash
# Проверка healthcheck
docker inspect systech-aidd-postgres | grep -A 10 "Health"

# Подключение к базе данных
docker exec -it systech-aidd-postgres psql -U aidd_user -d aidd_db -c "SELECT version();"
```

### 3. Проверка доступности API

```bash
# Проверка health endpoint
curl -f http://localhost:8001/health

# Проверка через внешний IP
curl -f http://83.147.246.172:8001/health
```

### 4. Проверка доступности Frontend

```bash
# Проверка локально
curl -I http://localhost:3001

# Проверка через внешний IP
curl -I http://83.147.246.172:3001
```

### 5. Проверка работы бота

1. Откройте Telegram
2. Найдите вашего бота
3. Отправьте команду `/start`
4. Отправьте тестовое сообщение
5. Проверьте логи бота:

```bash
docker compose -f docker-compose.prod.yml logs bot
```

### 6. Проверка миграций

```bash
# Проверка логов миграций
docker compose -f docker-compose.prod.yml logs migrations

# Проверка таблиц в базе данных
docker exec -it systech-aidd-postgres psql -U aidd_user -d aidd_db -c "\dt"
```

---

## 🔍 Troubleshooting

### Проблема: Контейнер не запускается

```bash
# Проверка логов
docker compose -f docker-compose.prod.yml logs [service_name]

# Проверка конфигурации
docker compose -f docker-compose.prod.yml config

# Перезапуск сервиса
docker compose -f docker-compose.prod.yml restart [service_name]
```

### Проблема: Порты заняты

```bash
# Проверка занятых портов
sudo netstat -tlnp | grep :8001
sudo netstat -tlnp | grep :3001

# Остановка сервисов, использующих порты
sudo systemctl stop [service_name]
```

### Проблема: Недостаточно ресурсов

```bash
# Проверка использования ресурсов
docker stats

# Очистка неиспользуемых образов
docker image prune -f

# Очистка неиспользуемых контейнеров
docker container prune -f
```

### Проблема: Ошибки в логах

```bash
# Поиск ошибок в логах
docker compose -f docker-compose.prod.yml logs | grep -i error
docker compose -f docker-compose.prod.yml logs | grep -i exception
docker compose -f docker-compose.prod.yml logs | grep -i failed
```

### Проблема: База данных недоступна

```bash
# Проверка статуса PostgreSQL
docker compose -f docker-compose.prod.yml logs postgres

# Перезапуск PostgreSQL
docker compose -f docker-compose.prod.yml restart postgres

# Проверка подключения
docker exec -it systech-aidd-postgres pg_isready -U aidd_user -d aidd_db
```

### Проблема: CORS ошибки в браузере

```bash
# Проверка переменной CORS_ORIGINS
grep CORS_ORIGINS .env

# Проверка CORS headers
curl -H "Origin: http://83.147.246.172:3001" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     http://83.147.246.172:8001/api/v1/statistics

# Перезапуск API после изменения CORS
docker compose -f docker-compose.prod.yml restart api
```

---

## 📊 Мониторинг и обслуживание

### 1. Просмотр логов

```bash
# Все сервисы
docker compose -f docker-compose.prod.yml logs -f

# Конкретный сервис
docker compose -f docker-compose.prod.yml logs -f [service_name]

# Последние 100 строк
docker compose -f docker-compose.prod.yml logs --tail=100 [service_name]
```

### 2. Обновление сервисов

```bash
# Загрузка новых образов
docker compose -f docker-compose.prod.yml pull

# Перезапуск с новыми образами
docker compose -f docker-compose.prod.yml up -d
```

### 3. Остановка сервисов

```bash
# Остановка всех сервисов
docker compose -f docker-compose.prod.yml down

# Остановка с удалением volumes (ОСТОРОЖНО!)
docker compose -f docker-compose.prod.yml down -v
```

### 4. Резервное копирование

```bash
# Создание бэкапа базы данных
docker exec systech-aidd-postgres pg_dump -U aidd_user aidd_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Создание бэкапа volumes
docker run --rm -v systech-aidd_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_data_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
```

---

## 🎯 Чеклист завершения

- [ ] SSH подключение работает
- [ ] Все файлы скопированы на сервер
- [ ] .env файл настроен с реальными значениями
- [ ] Docker образы загружены
- [ ] Все контейнеры запущены и работают
- [ ] PostgreSQL healthcheck проходит
- [ ] Миграции применены успешно
- [ ] API доступен через http://83.147.246.172:8001/health
- [ ] Frontend доступен через http://83.147.246.172:3001
- [ ] Bot отвечает в Telegram
- [ ] Логи не содержат критических ошибок

---

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи сервисов
2. Убедитесь в правильности конфигурации
3. Проверьте доступность внешних ресурсов (OpenRouter API)
4. Убедитесь в корректности токенов и ключей

**Успешного развертывания! 🚀**
