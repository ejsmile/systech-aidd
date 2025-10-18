# Функциональные требования к дашборду

> **Базовый документ:** [roadmap.md](../roadmap.md)

## Обзор

Дашборд предоставляет администраторам системы визуальный обзор статистики использования Telegram бота. Целевая аудитория - технические специалисты и администраторы системы.

## Источник данных

Данные извлекаются из PostgreSQL базы данных:
- Таблица `users` - информация о пользователях
- Таблица `messages` - история сообщений

### Схема БД

**users:**
- `user_id` (BigInteger, PK) - Telegram ID пользователя
- `username` (String) - Telegram username
- `first_name` (String) - Имя
- `last_name` (String) - Фамилия
- `created_at` (DateTime) - Дата регистрации
- `updated_at` (DateTime) - Дата последнего обновления

**messages:**
- `id` (BigInteger, PK) - ID сообщения
- `chat_id` (BigInteger) - ID чата
- `user_id` (BigInteger) - ID пользователя
- `role` (String) - Роль (user/assistant/system)
- `content` (Text) - Содержимое сообщения
- `created_at` (DateTime) - Дата создания
- `deleted_at` (DateTime, nullable) - Дата удаления (soft delete)

## Ключевые метрики

### 1. Общее количество пользователей
**Описание:** Всего уникальных пользователей, зарегистрированных в системе  
**Источник:** `SELECT COUNT(*) FROM users`  
**Формат:** Целое число  
**Пример:** 125

### 2. Активные пользователи
**Описание:** Пользователи, отправившие хотя бы одно сообщение за последние 30 дней  
**Источник:** `SELECT COUNT(DISTINCT user_id) FROM messages WHERE created_at > NOW() - INTERVAL '30 days' AND deleted_at IS NULL`  
**Формат:** Целое число  
**Пример:** 42

### 3. Общее количество сообщений
**Описание:** Всего сообщений в системе (не удаленных)  
**Источник:** `SELECT COUNT(*) FROM messages WHERE deleted_at IS NULL`  
**Формат:** Целое число  
**Пример:** 3540

### 4. Среднее количество сообщений на пользователя
**Описание:** Среднее количество сообщений на одного активного пользователя  
**Источник:** `total_messages / active_users`  
**Формат:** Число с плавающей точкой (1 знак после запятой)  
**Пример:** 28.4

### 5. Распределение сообщений по датам
**Описание:** Количество сообщений по дням за последние 30 дней  
**Источник:** 
```sql
SELECT DATE(created_at) as date, COUNT(*) as count 
FROM messages 
WHERE created_at > NOW() - INTERVAL '30 days' AND deleted_at IS NULL
GROUP BY DATE(created_at) 
ORDER BY date ASC
```
**Формат:** Массив объектов `{date: datetime, count: int}`  
**Пример:**
```json
[
  {"date": "2025-09-18", "count": 45},
  {"date": "2025-09-19", "count": 52},
  {"date": "2025-09-20", "count": 38}
]
```

### 6. Топ-10 активных пользователей
**Описание:** 10 пользователей с наибольшим количеством сообщений  
**Источник:**
```sql
SELECT u.user_id, u.username, COUNT(m.id) as message_count
FROM users u
LEFT JOIN messages m ON u.user_id = m.user_id AND m.deleted_at IS NULL
GROUP BY u.user_id, u.username
ORDER BY message_count DESC
LIMIT 10
```
**Формат:** Массив объектов `{user_id: int, username: str | null, message_count: int}`  
**Пример:**
```json
[
  {"user_id": 123456, "username": "john_doe", "message_count": 245},
  {"user_id": 789012, "username": "jane_smith", "message_count": 198},
  {"user_id": 345678, "username": null, "message_count": 156}
]
```

## Структура дашборда

### Верхний блок: Карточки метрик
Четыре карточки в один ряд (responsive grid):
1. Общее количество пользователей
2. Активные пользователи
3. Общее количество сообщений
4. Среднее сообщений/пользователь

### Средний блок: График
Линейный или столбчатый график:
- **X-ось:** Даты (последние 30 дней)
- **Y-ось:** Количество сообщений
- **Интерактивность:** Tooltip при наведении

### Нижний блок: Таблица
Таблица топ-10 пользователей:
- **Колонки:** Позиция, User ID, Username, Количество сообщений
- **Сортировка:** По количеству сообщений (по убыванию)

## Требования к UX/UI

### Дизайн
- Modern, clean интерфейс
- Светлая тема (опционально темная тема позже)
- Использование UI библиотеки (Shadcn/ui, Chakra UI)
- Consistent color scheme

### Responsive дизайн
- Desktop: карточки в 4 колонки
- Tablet: карточки в 2 колонки
- Mobile: карточки в 1 колонку

### Loading states
- Skeleton loaders для карточек
- Loading spinner для графика
- Progress indicator для таблицы

### Error handling
- Graceful error messages
- Retry кнопка при ошибке загрузки
- Fallback UI при отсутствии данных

### Performance
- Загрузка данных < 2 секунд
- Smooth transitions и анимации
- Оптимизация рендеринга графиков

## Дополнительные требования

### Accessibility
- Семантический HTML
- ARIA labels где необходимо
- Keyboard navigation support

### Browser support
- Chrome (последние 2 версии)
- Firefox (последние 2 версии)
- Safari (последние 2 версии)
- Edge (последние 2 версии)

## Будущие расширения (вне текущего спринта)

- Фильтры по датам (date range picker)
- Экспорт данных в CSV/Excel
- Real-time обновление через WebSocket
- Детализация по конкретному пользователю
- Графики по типам сообщений (user vs assistant)

