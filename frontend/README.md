# Frontend - AIDD Dashboard & Chat

React + TypeScript веб-интерфейс для AIDD бота с дашбордом аналитики и floating AI-чатом.

## 🚀 Быстрый старт

```bash
# Установить зависимости
npm install

# Запустить dev сервер
npm run dev
# Откроется на http://localhost:5173

# Собрать для продакшена
npm run build

# Preview production build
npm run preview
```

## 🎯 Основные возможности

### 1. **Floating AI Chat** 
Глобальный чат-помощник, доступный на всех страницах:
- 🔘 **Floating кнопка** в правом нижнем углу с badge индикатором режима
- 💬 **Два режима работы:**
  - **Обычный режим (AI)**: общение с LLM-ассистентом
  - **Админ режим (SQL)**: Text2SQL запросы к базе данных
- 📱 **Адаптивный дизайн:** 
  - Desktop: floating окно 400x600px
  - Mobile: full screen overlay
- ⚡ **Фичи:**
  - История диалогов с автоскроллом
  - Авто-ресайз textarea при вводе
  - Очистка истории
  - Поддержка темной/светлой темы

### 2. **Dashboard Analytics**
Визуализация статистики использования бота:
- 📊 **Метрики**: пользователи, сообщения, средние значения
- 📈 **График динамики** сообщений по датам
- 👥 **Таблица топ пользователей**
- 🔄 **Автообновление** каждые 30 секунд
- 📅 **Фильтрация по периодам**: неделя / месяц / весь период

### 3. **Dark/Light Theme**
Полная поддержка темной и светлой темы:
- 🌓 Автоматическое определение системных предпочтений
- 💾 Сохранение выбора в localStorage
- 🎨 CSS переменные (design tokens) для обеих тем
- 🔄 Переключатель темы в UI

## 📁 Структура проекта

```
frontend/src/
├── components/              # Переиспользуемые компоненты
│   ├── FloatingChat.tsx              # Обертка floating чата
│   ├── FloatingChatButton.tsx        # Кнопка в правом нижнем углу
│   ├── FloatingChatWindow.tsx        # Окно чата
│   ├── ChatMessage.tsx               # Отображение сообщения
│   ├── SQLResultDisplay.tsx          # Отображение SQL результатов
│   ├── ThemeToggle.tsx               # Переключатель темы
│   ├── PeriodSelector.tsx            # Выбор периода
│   ├── MetricCard.tsx                # Карточка метрики
│   ├── MessagesByDateChart.tsx       # График сообщений
│   ├── TopUsersTable.tsx             # Таблица топ пользователей
│   ├── Header.tsx                    # Шапка приложения
│   ├── Sidebar.tsx                   # Боковая навигация
│   ├── Layout.tsx                    # Layout wrapper
│   └── ui/                           # Shadcn/ui компоненты
│       ├── button.tsx
│       ├── card.tsx
│       ├── select.tsx
│       ├── alert.tsx
│       ├── table.tsx
│       ├── skeleton.tsx
│       ├── chat-input.tsx            # Chat input из референса
│       └── textarea.tsx              # Textarea из референса
├── pages/                   # Страницы приложения
│   └── Dashboard.tsx                 # Дашборд со статистикой
├── contexts/                # React Context API
│   └── ThemeContext.tsx              # Управление темой
├── hooks/                   # Custom React hooks
│   └── use-textarea-resize.ts        # Hook для авто-ресайза textarea
├── api/                     # API клиент для backend
│   ├── client.ts                     # Базовый HTTP клиент
│   ├── chat.ts                       # API методы для чата
│   └── statistics.ts                 # API методы для статистики
├── types/                   # TypeScript типы
│   ├── chat.ts                       # Типы для чата
│   └── statistics.ts                 # Типы для статистики
├── lib/                     # Утилиты
│   └── utils.ts                      # cn() для Tailwind CSS
├── App.tsx                  # Главный компонент с роутингом
├── main.tsx                 # Entry point
└── index.css                # Tailwind CSS + CSS переменные
```

## 🛠 Технологический стек

### Основные технологии
- **React 18** - UI библиотека
- **TypeScript 5** - type safety для JavaScript
- **Vite 7** - быстрая сборка и dev сервер
- **React Router 6** - клиентский роутинг

### UI & Стилизация
- **Tailwind CSS 4** - utility-first CSS фреймворк
- **Shadcn/ui** - современные UI компоненты (Radix UI + Tailwind)
- **Radix UI** - примитивы для доступных компонентов
- **Lucide React** - иконки (MessageCircle, Moon, Sun, X, Trash2, etc.)
- **Recharts** - декларативные графики для React

### Quality & Testing
- **ESLint** - линтинг JavaScript/TypeScript
- **Prettier** - форматирование кода
- **TypeScript strict mode** - строгая проверка типов
- **Vitest** - unit тестирование
- **React Testing Library** - тестирование компонентов

### Зависимости (package.json)
```json
{
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "react-router-dom": "^7.9.4",
    "@radix-ui/react-select": "^2.2.6",
    "@radix-ui/react-slot": "^1.2.3",
    "lucide-react": "^0.546.0",
    "recharts": "^3.3.0",
    "tailwindcss": "^4.1.14",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "tailwind-merge": "^3.3.1"
  }
}
```

## 📝 Доступные команды

```bash
# Разработка
npm run dev              # Запустить dev сервер (http://localhost:5173)

# Сборка
npm run build            # Собрать для продакшена (в dist/)
npm run preview          # Preview production build

# Качество кода
npm run lint             # ESLint проверка
npm run lint:fix         # ESLint автофикс
npm run format           # Prettier форматирование
npm run format:check     # Prettier проверка

# Тестирование
npm run test             # Запустить тесты (watch mode)
npm run test:ui          # Тесты с UI
npm run test:run         # Тесты без watch mode
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в директории `frontend/`:

```bash
# Backend API URL
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Tailwind CSS

Конфигурация в `tailwind.config.js`:
- Dark mode support через `class` стратегию
- CSS переменные для цветов (design tokens)
- Кастомные цвета для графиков

### Shadcn/ui

Конфигурация в `components.json`:
- Компоненты в `src/components/ui/`
- Утилиты в `src/lib/utils.ts`
- Tailwind CSS prefix: не используется

## 🎨 Дизайн система

### Цветовая палитра
- **primary** - основной цвет (синий)
- **secondary** - вторичный цвет (серый)
- **muted** - приглушенный (для backgrounds)
- **accent** - акцентный (для hover состояний)
- **destructive** - деструктивный (красный, для ошибок)
- **card** - цвет карточек
- **popover** - цвет popover/dropdown

### Графики
- **chart-1** до **chart-5** - цвета для графиков Recharts

### Темная/светлая тема
Все цвета поддерживают обе темы через CSS переменные в `index.css`.

## 🚦 API Endpoints

Frontend использует следующие API endpoints:

### Statistics
```typescript
GET /api/v1/statistics
  ?start_date=2024-01-01T00:00:00Z
  &end_date=2024-12-31T23:59:59Z
```

### Chat
```typescript
// Отправить сообщение
POST /api/v1/chat/message
{ user_id: string, message: string }

// Получить историю
GET /api/v1/chat/history/:user_id

// Очистить историю
DELETE /api/v1/chat/history/:user_id

// Text2SQL запрос (админ режим)
POST /api/v1/admin/query
{ query: string }
```

Подробная документация API: см. `docs/api/api-contract.md` в корне проекта.

## 📚 Дополнительные документы

- **[docs/front-vision.md](docs/front-vision.md)** - видение frontend приложения
- **[docs/tech-stack.md](docs/tech-stack.md)** - детальное описание технологического стека
- **[../docs/api/api-contract.md](../docs/api/api-contract.md)** - API контракт
- **[../docs/frontend/dashboard-requirements.md](../docs/frontend/dashboard-requirements.md)** - требования к дашборду

## 🧪 Тестирование

```bash
# Запустить тесты
npm run test

# Тесты с UI
npm run test:ui

# Тесты один раз (CI)
npm run test:run
```

Тесты используют:
- **Vitest** - тестовый раннер
- **React Testing Library** - тестирование компонентов
- **@testing-library/user-event** - симуляция пользовательских действий

## 💡 Принципы разработки

- **Component Composition** - компоненты через композицию
- **TypeScript Strict Mode** - все с type hints
- **Responsive First** - mobile-first подход
- **Accessibility** - доступность через Radix UI
- **Dark Mode Support** - поддержка темной темы во всех компонентах
- **Code Quality** - ESLint + Prettier + TypeScript

## 🐛 Troubleshooting

### Порт занят

Если порт 5173 занят, Vite автоматически попробует 5174, 5175 и т.д.

### API недоступен

Убедитесь, что backend API запущен:
```bash
cd ..  # в корень проекта
make run-api
```

### Ошибки TypeScript

Проверьте `tsconfig.json` и убедитесь, что все зависимости установлены:
```bash
npm install
```

## 📄 Лицензия

См. [LICENSE](../LICENSE) в корне проекта.
