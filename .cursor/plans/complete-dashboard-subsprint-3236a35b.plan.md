<!-- 3236a35b-3c79-4d50-81bb-00145404daa5 2d8a5f07-a5d9-4392-a57b-6c8cb3223fcf -->
# Завершение реализации Dashboard (Подспринт 3)

## Обзор

Реализация итераций 3.1-3.4 из tasklist-sp3.md: улучшение layout, метрики Dashboard, визуализация и интеграция с API.

## Этапы реализации

### 1. Добавление необходимых shadcn/ui компонентов (Подготовка к итерации 3.1)

Добавить компоненты shadcn/ui, необходимые для Dashboard:

- Card (для карточек метрик и контейнеров)
- Table (для топ пользователей)
- Alert (для состояний ошибок)
- Skeleton (для состояний загрузки)
```bash
# Выполнить из директории frontend
npx shadcn@latest add card table alert skeleton
```


### 2. Улучшение Layout и навигации (Итерация 3.1)

**Файлы для изменения:**

- `frontend/src/App.tsx` - Удалить тестовый компонент SampleChart
- Создать `frontend/src/components/Layout.tsx` - Вынести layout в отдельный компонент
- Создать `frontend/src/components/Sidebar.tsx` - Вынести sidebar
- Создать `frontend/src/components/Header.tsx` - Добавить header с заголовком страницы

**Улучшения layout:**

- Вынести Layout, Sidebar, Header в отдельные компоненты для лучшей организации
- Добавить компонент Header, отображающий заголовок текущей страницы
- Сохранить responsive дизайн
- Очистить App.tsx, оставив только роутинг

### 3. Создание компонента MetricCard (Итерация 3.2)

**Создать:** `frontend/src/components/MetricCard.tsx`

Компонент MetricCard отображает:

- Заголовок (например, "Total Users")
- Значение (большое число)
- Опциональное описание/подзаголовок
- Иконку (опционально)
- Состояние загрузки (skeleton)

Использует shadcn компонент Card со стилями Tailwind.

### 4. Реализация Dashboard с метриками (Итерация 3.2)

**Изменить:** `frontend/src/pages/Dashboard.tsx`

Реализовать страницу Dashboard с:

- Сеткой 2x2 из компонентов MetricCard, показывающих:
  - Всего пользователей (Total Users)
  - Активных пользователей (Active Users)
  - Всего сообщений (Total Messages)
  - Среднее сообщений на пользователя (Avg Messages Per User)
- Состоянием загрузки (показать скелетоны)
- Состоянием ошибки (показать компонент Alert)
- Использовать React hooks (useState, useEffect) для загрузки данных

### 5. Создание компонента графика сообщений (Итерация 3.3)

**Создать:** `frontend/src/components/MessagesByDateChart.tsx`

Компонент графика с использованием Recharts:

- LineChart или BarChart для сообщений по датам
- ResponsiveContainer для responsive дизайна
- Правильные подписи осей и tooltips
- Использует `messages_by_date` из ответа API
- Корректная обработка пустых данных

Использовать существующий `SampleChart.tsx` как референс для паттернов Recharts.

### 6. Создание компонента таблицы топ пользователей (Итерация 3.3)

**Создать:** `frontend/src/components/TopUsersTable.tsx`

Компонент таблицы с использованием shadcn Table:

- Отображение топ 10 пользователей по количеству сообщений
- Колонки: Ранг, User ID, Username, Количество сообщений
- Обработка null username (показать "Unknown")
- Responsive дизайн

### 7. Интеграция графиков в Dashboard (Итерация 3.3)

**Изменить:** `frontend/src/pages/Dashboard.tsx`

Добавить в Dashboard ниже метрик:

- MessagesByDateChart в Card
- TopUsersTable в Card
- Правильные отступы и layout
- Оба компонента получают данные из API

### 8. Подключение Dashboard к API (Итерация 3.4)

**Изменить:** `frontend/src/pages/Dashboard.tsx`

Реализовать загрузку данных:

- Вызов `getStatistics()` при монтировании компонента
- Обработка состояния загрузки (показать Skeletons)
- Обработка состояния ошибки (показать Alert с кнопкой retry)
- Обновление состояния полученными данными
- Передача данных в компоненты MetricCard, Chart и Table

**Обработка ошибок:**

```typescript
try {
  const data = await getStatistics()
  setStatistics(data)
} catch (error) {
  setError(error instanceof APIError ? error.message : 'Failed to load')
}
```

### 9. Добавление автообновления (Улучшение итерации 3.4)

**Изменить:** `frontend/src/pages/Dashboard.tsx`

Опциональное улучшение:

- Добавить автообновление каждые 30 секунд через `setInterval`
- Показать время последнего обновления
- Очистка интервала при размонтировании компонента

### 10. Финальное тестирование и очистка

- Удалить `SampleChart.tsx` и его использование (больше не нужен)
- Тестирование с запущенным API (`make run-api`)
- Тестирование состояний загрузки
- Тестирование состояний ошибки (остановить API)
- Тестирование responsive дизайна на разных размерах экрана
- Проверить правильность отображения всех метрик
- Запустить линтер: `npm run lint` в frontend/
- Обновить статус в tasklist-sp3.md на ✅ для итераций 3.1-3.4

## Ключевые файлы

**Новые файлы:**

- `frontend/src/components/Layout.tsx`
- `frontend/src/components/Sidebar.tsx`
- `frontend/src/components/Header.tsx`
- `frontend/src/components/MetricCard.tsx`
- `frontend/src/components/MessagesByDateChart.tsx`
- `frontend/src/components/TopUsersTable.tsx`

**Изменяемые файлы:**

- `frontend/src/App.tsx` - Использовать вынесенный Layout
- `frontend/src/pages/Dashboard.tsx` - Полная реализация

**Удаляемые файлы:**

- `frontend/src/components/SampleChart.tsx` - Больше не нужен

## Чеклист тестирования

- [ ] `make run-api` запускает backend на порту 8000
- [ ] `make frontend-dev` запускает frontend на порту 5173
- [ ] Dashboard загружается и отображает 4 карточки метрик
- [ ] График показывает распределение сообщений по времени
- [ ] Таблица показывает топ 10 пользователей
- [ ] Скелетоны загрузки появляются во время загрузки данных
- [ ] Alert с ошибкой появляется когда API недоступен
- [ ] Навигация между Dashboard и Chat работает
- [ ] Responsive дизайн работает на mobile/tablet/desktop
- [ ] Нет ошибок в консоли или ошибок TypeScript
- [ ] Линтер проходит: `cd frontend && npm run lint`

### To-dos

- [ ] Add shadcn/ui components: Card, Table, Alert, Skeleton
- [ ] Extract Layout, Sidebar, Header to separate components and clean up App.tsx
- [ ] Create MetricCard component with loading skeleton state
- [ ] Implement Dashboard.tsx with 4 metric cards and data fetching logic
- [ ] Create MessagesByDateChart component using Recharts
- [ ] Create TopUsersTable component using shadcn Table
- [ ] Add chart and table components to Dashboard page
- [ ] Connect Dashboard to getStatistics() API with error handling
- [ ] Add optional auto-refresh functionality (30s interval)
- [ ] Test all scenarios, clean up SampleChart, update tasklist-sp3.md