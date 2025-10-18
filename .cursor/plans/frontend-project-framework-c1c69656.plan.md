<!-- c1c69656-15a2-48a5-b65c-a2f315fb5203 06ed09ab-b57e-48e7-b6c0-5142584c0108 -->
# План: Подспринт 2 - Каркас frontend проекта

## Обзор

Создаем полноценный каркас frontend приложения на базе React 18 + TypeScript + Vite с настроенными инструментами разработки, структурой проекта и базовым UI.

## Выбранные технологии

- **Frontend Framework:** React 18 + TypeScript
- **Build Tool:** Vite
- **UI Library:** Shadcn/ui (Radix UI + Tailwind CSS)
- **Charts:** Recharts
- **State Management:** React Context API
- **HTTP Client:** fetch API
- **Testing:** Vitest + React Testing Library
- **Linting/Formatting:** ESLint + Prettier

## Что уже готово

- `docs/frontend/dashboard-requirements.md` - функциональные требования
- Backend API готов и работает (`src/api/`)

## Итерация 2.1: Дополнить документацию frontend

### Создать `frontend/docs/front-vision.md`

Документ с видением frontend приложения:

- Целевая аудитория: администраторы системы
- Основные экраны: Dashboard (статистика), Chat (веб-чат с ботом)
- Принципы UX/UI: modern, clean, responsive
- Требования к производительности и доступности

### Создать `frontend/docs/tech-stack.md`

Документация выбранного технологического стека с обоснованием:

- React 18 + TypeScript - type safety, популярность
- Vite - быстрая сборка
- Shadcn/ui - modern UI, настраиваемость
- Recharts - декларативные графики, React-native API
- React Context - простой state management (KISS)
- fetch API - встроенный, без лишних зависимостей
- Vitest - fast unit testing, Vite integration

## Итерация 2.2: Инициализация Vite проекта

### Создать frontend проект

```bash
cd /Users/pavelkarasov/Source/systech-aidd-my
npm create vite@latest frontend -- --template react-ts
```

### Структура после инициализации

```
frontend/
├── docs/
│   ├── front-vision.md
│   └── tech-stack.md
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   └── ...
├── package.json
├── tsconfig.json
├── vite.config.ts
└── index.html
```

## Итерация 2.3: Настройка инструментов разработки

### TypeScript конфигурация

Обновить `frontend/tsconfig.json`:

- `strict: true`
- path aliases: `@/*` → `./src/*`
- React 18 JSX runtime

### ESLint + Prettier

Установить и настроить:

- `eslint` с React plugin
- `prettier` для форматирования
- Создать `.eslintrc.cjs` и `.prettierrc`
- Добавить скрипты в `package.json`

### Tailwind CSS

Установить для Shadcn/ui:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Настроить `tailwind.config.js` с темой и путями к компонентам.

### Shadcn/ui setup

```bash
npx shadcn-ui@latest init
```

- Выбрать стиль, цвета
- Настроить `components.json`

## Итерация 2.4: Создать структуру директорий

### Директории в `frontend/src/`:

```
src/
├── components/     # Переиспользуемые UI компоненты
│   └── ui/        # Shadcn/ui компоненты (автогенерируемые)
├── pages/         # Страницы приложения
│   ├── Dashboard.tsx
│   └── Chat.tsx
├── api/           # API клиент для backend
│   ├── client.ts
│   └── statistics.ts
├── types/         # TypeScript типы и интерфейсы
│   └── statistics.ts
├── hooks/         # Custom React hooks
├── utils/         # Утилитные функции
├── App.tsx
└── main.tsx
```

### Создать placeholder файлы

- `src/pages/Dashboard.tsx` - заглушка страницы дашборда
- `src/pages/Chat.tsx` - заглушка страницы чата
- `src/api/client.ts` - базовый API клиент
- `src/types/statistics.ts` - TypeScript типы для API

## Итерация 2.5: Базовый App компонент

### Обновить `src/App.tsx`

- Простая структура с заголовком
- Заглушка для навигации (Dashboard / Chat)
- Базовые стили через Tailwind

### Установить React Router

```bash
npm install react-router-dom
```

Настроить роутинг:

- `/` → Dashboard
- `/chat` → Chat

### Тестовый запуск

Убедиться что приложение запускается без ошибок.

## Итерация 2.6: Установить зависимости для графиков

### Recharts

```bash
npm install recharts
```

### Создать пример компонента с графиком

`src/components/SampleChart.tsx` - простой тестовый график для проверки работы Recharts.

## Итерация 2.7: Настройка Vitest для тестирования

### Установить зависимости

```bash
npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom
```

### Настроить `vite.config.ts`

Добавить конфигурацию для Vitest:

```ts
test: {
  globals: true,
  environment: 'jsdom',
  setupFiles: './src/setupTests.ts',
}
```

### Создать `src/setupTests.ts`

Настройка окружения для тестов (импорт `@testing-library/jest-dom`).

### Написать пример теста

`src/App.test.tsx` - простой smoke test для App компонента.

## Итерация 2.8: Обновить Makefile

### Добавить команды для frontend

```makefile
# Frontend commands
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

frontend-preview:
	cd frontend && npm run preview

frontend-lint:
	cd frontend && npm run lint

frontend-test:
	cd frontend && npm test
```

## Итерация 2.9: Обновить README.md

### Добавить секцию Frontend

- Инструкции по установке зависимостей
- Команды для запуска dev сервера
- Команды для сборки и тестирования
- Структура проекта

### Примеры команд

```bash
# Установка зависимостей
make frontend-install

# Запуск dev сервера (http://localhost:5173)
make frontend-dev

# Сборка для продакшена
make frontend-build

# Тестирование
make frontend-test

# Линтинг
make frontend-lint
```

## Проверка готовности

### Чеклист

- [ ] Vite проект инициализирован
- [ ] TypeScript настроен (strict mode)
- [ ] ESLint + Prettier работают
- [ ] Tailwind CSS установлен
- [ ] Shadcn/ui настроен
- [ ] Recharts установлен
- [ ] React Router настроен
- [ ] Структура директорий создана
- [ ] Базовый App компонент работает
- [ ] Vitest настроен, example тест проходит
- [ ] Makefile команды добавлены
- [ ] README обновлен
- [ ] `make frontend-dev` запускает приложение на http://localhost:5173
- [ ] Нет TypeScript ошибок
- [ ] Нет ESLint warnings

### Финальная проверка

```bash
# 1. Установка
make frontend-install

# 2. Запуск
make frontend-dev
# Открыть http://localhost:5173
# Проверить что приложение отображается

# 3. Линтинг
make frontend-lint
# Не должно быть ошибок

# 4. Тестирование
make frontend-test
# Тесты должны пройти

# 5. Сборка
make frontend-build
# Сборка должна пройти успешно
```

## Результат

После выполнения плана получим:

- Полностью настроенный frontend проект
- Рабочий dev-сервер на Vite
- Настроенные инструменты разработки (ESLint, Prettier, TypeScript)
- Базовую структуру приложения с роутингом
- Готовность к реализации Dashboard и Chat компонентов (Подспринт 3 и 4)

### To-dos

- [ ] Создать frontend/docs/front-vision.md с описанием видения, целевой аудитории, экранов и требований
- [ ] Создать frontend/docs/tech-stack.md с документацией выбранного стека и обоснованием
- [ ] Инициализировать Vite проект с React + TypeScript шаблоном в директории frontend/
- [ ] Настроить TypeScript (strict mode, path aliases, React 18 JSX)
- [ ] Установить и настроить ESLint + Prettier с React плагинами
- [ ] Установить и настроить Tailwind CSS для Shadcn/ui
- [ ] Инициализировать Shadcn/ui через CLI и настроить компоненты
- [ ] Создать структуру директорий (components/, pages/, api/, types/, hooks/, utils/)
- [ ] Создать placeholder файлы для страниц, API клиента и типов
- [ ] Установить React Router и настроить базовый роутинг (/, /chat)
- [ ] Обновить App.tsx с роутингом и базовой структурой
- [ ] Установить Recharts и создать тестовый компонент с графиком
- [ ] Установить Vitest, React Testing Library, настроить конфигурацию и создать пример теста
- [ ] Добавить команды для frontend в Makefile (install, dev, build, test, lint)
- [ ] Обновить README.md с секцией Frontend и инструкциями по использованию
- [ ] Выполнить финальную проверку: запуск, линтинг, тестирование, сборка