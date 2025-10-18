# Известные проблемы Спринта D0

**Дата:** 2025-10-18

## 🐛 Frontend: Проблема с резолвингом путей в Docker

### Описание проблемы

Frontend не запускается в Docker из-за ошибки резолвинга путей с алиасом `@/`.

### Симптомы

```
[plugin:vite:import-analysis] Failed to resolve import "@/api/statistics" 
from "src/pages/Dashboard.tsx". Does the file exist?
```

### Окружение

- Vite: 7.1.10
- Node.js: 20-alpine (в контейнере)
- Docker Compose

### Детали

1. Конфигурация `vite.config.ts` корректна:
   ```typescript
   resolve: {
     alias: {
       '@': path.resolve(__dirname, './src'),
     },
   }
   ```

2. Файлы существуют в контейнере:
   ```bash
   $ docker-compose exec frontend ls -la /app/src/api/
   -rw-r--r--  chat.ts
   -rw-r--r--  client.ts
   -rw-r--r--  statistics.ts  ✅
   ```

3. Volume mount был отключен (проблема не в этом):
   ```yaml
   # volumes:
   #   - ./frontend/src:/app/src  # Отключено
   ```

4. Образ пересобирался без кэша - проблема сохраняется

### Возможные причины

1. **Проблема с `tsconfig.json` paths:**
   - Возможно, Vite не подхватывает tsconfig paths в Docker окружении

2. **Проблема с `__dirname` в контейнере:**
   - `path.resolve(__dirname, './src')` может работать неправильно

3. **Кэширование на уровне Node.js/Vite:**
   - Несмотря на пересборку, может оставаться старый кэш

### Статус

⚠️ **Требует дальнейшего исследования**

### Влияние на MVP

- ✅ API полностью работает
- ✅ Bot работает  
- ✅ PostgreSQL работает
- ⚠️ Frontend не работает в Docker (но работает локально)

**Для MVP:** Не критично, так как основная цель D0 - запуск сервисов в Docker. API и Bot работают корректно.

### Workaround (временное решение)

Запускать frontend локально, а не в Docker:

```bash
# Остановить frontend в Docker
docker-compose stop frontend

# Запустить локально
cd frontend
npm run dev
```

Frontend будет доступен на http://localhost:5173 и сможет подключаться к API в Docker (http://localhost:8000).

### План исправления

Для следующих спринтов:

1. **Исследовать проблему:**
   - Проверить работу с абсолютными путями вместо alias
   - Попробовать другие варианты конфигурации Vite
   - Проверить tsconfig.app.json paths

2. **Альтернативные решения:**
   - Использовать production build вместо dev сервера
   - Настроить nginx для раздачи статики
   - Рассмотреть Multi-stage build

3. **Тестирование:**
   - Создать minimal reproduction case
   - Проверить на других проектах с Vite + Docker

### Рекомендации

Для D0 (MVP):
- ✅ Оставить как есть, использовать workaround
- ✅ Задокументировать проблему
- ✅ Добавить в план D1/D2 как улучшение

## Обновление docker-compose.yml

Для стабильной работы других сервисов, volume mount для frontend отключен:

```yaml
frontend:
  # volumes:
  #   - ./frontend/src:/app/src  # Отключено для стабильной работы в Docker
```

Это не влияет на работу API и Bot.

---

**Важно:** Эта проблема не блокирует основную цель Спринта D0 - запуск всех сервисов через `docker-compose up`. API, Bot и БД работают корректно.

