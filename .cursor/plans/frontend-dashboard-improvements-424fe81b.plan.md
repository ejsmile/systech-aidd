<!-- 424fe81b-a824-4bb3-a026-02711e6ed60e dd3e2781-226f-4d63-a1aa-82fb6ab7c7b1 -->
# Улучшения фронтенда дашборда

## 1. График: усиление линии между точками

**Файл:** `frontend/src/components/MessagesByDateChart.tsx`

Текущий график уже имеет линию (`Line` component), но нужно сделать ее более заметной:

- Увеличить `strokeWidth` с 2 до 3-4
- Убрать или уменьшить размер точек (`dot` prop)
- Добавить `activeDot` для интерактивности при наведении
```68:76:frontend/src/components/MessagesByDateChart.tsx
<Line
  type="monotone"
  dataKey="count"
  stroke="hsl(var(--primary))"
  dot={{ fill: 'hsl(var(--primary))' }}
  strokeWidth={2}
  name="Messages"
  isAnimationActive={false}
/>
```


## 2. Удаление дублирования заголовков

### Файл 1: `frontend/src/App.tsx`

Убрать subtitle из Layout для Dashboard:

```15:15:frontend/src/App.tsx
<Layout title="Dashboard" subtitle="Статистика использования бота">
```

Изменить на: `<Layout title="Dashboard">`

### Файл 2: `frontend/src/pages/Dashboard.tsx`

Убрать дублирующийся заголовок h1, оставить только описание:

```63:71:frontend/src/pages/Dashboard.tsx
<div>
  <h1 className="text-3xl font-bold">Dashboard</h1>
  <p className="text-muted-foreground mt-2">
    Статистика использования бота и активности пользователей
  </p>
  <p className="text-muted-foreground mt-2 text-xs">
    Последнее обновление: {lastUpdate.toLocaleTimeString()}
  </p>
</div>
```

## 3. Date picker для выбора периода

### Создать новый компонент: `frontend/src/components/PeriodSelector.tsx`

- Dropdown с вариантами: "Неделя", "Месяц", "Весь период"
- Для "Весь период" можно добавить custom date picker (опционально на будущее)
- Компонент принимает callback для изменения периода
- Использовать shadcn/ui Select или DropdownMenu

### Изменить: `frontend/src/pages/Dashboard.tsx`

- Добавить state для выбранного периода
- Вычислять start_date и end_date на основе выбранного периода
- Передавать параметры в API запрос `getStatistics()`

### Изменить: `frontend/src/api/statistics.ts`

Обновить функцию для поддержки параметров:

```python
export async function getStatistics(
  startDate?: string,
  endDate?: string
): Promise<StatisticsResponse>
```

### Разместить компонент в Header

Изменить `frontend/src/components/Header.tsx` - добавить slot для правых контролов

## 4. Переключатель темы

### Создать компонент: `frontend/src/components/ThemeToggle.tsx`

- Кнопка/toggle для переключения между светлой и темной темой
- Использовать `useState` + `localStorage` для сохранения выбора
- Применять класс `dark` к корневому элементу HTML

### Создать контекст: `frontend/src/contexts/ThemeContext.tsx`

- Context для управления темой глобально
- Provider обертывает приложение в `main.tsx`

### Изменить: `frontend/src/components/Header.tsx`

Добавить ThemeToggle рядом с PeriodSelector в правой части

## 5. Темная тема

### Настроить: `frontend/src/index.css`

Добавить CSS переменные для светлой и темной темы (shadcn/ui convention):

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --muted: 210 40% 96.1%;
    --border: 214.3 31.8% 91.4%;
    /* ... другие переменные */
  }
  
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --muted: 217.2 32.6% 17.5%;
    --border: 217.2 32.6% 17.5%;
    /* ... другие переменные */
  }
}
```

### Обновить: `frontend/tailwind.config.js`

Добавить поддержку темной темы:

```js
module.exports = {
  darkMode: ["class"],
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: "hsl(var(--primary))",
        // ...
      }
    }
  }
}
```

### Адаптировать график: `frontend/src/components/MessagesByDateChart.tsx`

Убедиться что все цвета используют CSS переменные для корректного отображения в темной теме

## Структура изменений

**Новые файлы:**

- `frontend/src/components/PeriodSelector.tsx`
- `frontend/src/components/ThemeToggle.tsx`
- `frontend/src/contexts/ThemeContext.tsx`

**Изменяемые файлы:**

- `frontend/src/components/MessagesByDateChart.tsx`
- `frontend/src/components/Header.tsx`
- `frontend/src/pages/Dashboard.tsx`
- `frontend/src/App.tsx`
- `frontend/src/api/statistics.ts`
- `frontend/src/index.css`
- `frontend/tailwind.config.js`
- `frontend/src/main.tsx` (обернуть в ThemeProvider)