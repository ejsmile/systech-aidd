<!-- 7b459c62-a294-4699-b183-fe37dfe46b3c 3c724a4a-b397-4781-986c-42f93cf42012 -->
# Спринт 4 - Реализация ИИ-чата

## Цель

Интегрировать floating AI-чат в приложение на основе референса, удалить старую страницу /chat, добавить два режима работы (обычный и администратор).

## Архитектура

**Floating Chat структура:**

- FloatingChatButton - кнопка в правом нижнем углу
- FloatingChatWindow - раскрывающееся окно чата
- ChatInput (из референса) - компонент ввода с авто-ресайзом

**API endpoints (уже реализованы):**

- POST /api/v1/chat/message - отправка сообщения
- GET /api/v1/chat/history/{user_id} - получение истории
- DELETE /api/v1/chat/history/{user_id} - очистка истории
- POST /api/v1/admin/query - Text2SQL запросы

## Этапы реализации

### 1. Установка зависимостей из референса

Проверить наличие в `frontend/package.json`:

- `lucide-react` ✅ (уже есть)
- `@radix-ui/react-slot` ✅ (уже есть)
- `class-variance-authority` ✅ (уже есть)

Все необходимые зависимости уже установлены.

### 2. Создание компонентов из референса

**2.1. Hook для авто-ресайза textarea**

Создать `frontend/src/hooks/use-textarea-resize.ts`:

```typescript
import { useLayoutEffect, useRef } from "react";
import type { ComponentProps } from "react";

export function useTextareaResize(
  value: ComponentProps<"textarea">["value"],
  rows = 1,
) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  useLayoutEffect(() => {
    const textArea = textareaRef.current;
    if (textArea) {
      const computedStyle = window.getComputedStyle(textArea);
      const lineHeight = Number.parseInt(computedStyle.lineHeight, 10) || 20;
      const padding =
        Number.parseInt(computedStyle.paddingTop, 10) +
        Number.parseInt(computedStyle.paddingBottom, 10);
      
      const minHeight = lineHeight * rows + padding;
      textArea.style.height = "0px";
      const scrollHeight = Math.max(textArea.scrollHeight, minHeight);
      textArea.style.height = `${scrollHeight + 2}px`;
    }
  }, [textareaRef, value, rows]);
  
  return textareaRef;
}
```

**2.2. Textarea UI компонент**

Создать `frontend/src/components/ui/textarea.tsx`:

```typescript
import * as React from "react";
import { cn } from "@/lib/utils";

const Textarea = React.forwardRef<HTMLTextAreaElement, React.ComponentProps<"textarea">>(
  ({ className, ...props }, ref) => {
    return (
      <textarea
        className={cn(
          "flex min-h-[80px] w-full rounded-lg border border-input bg-background px-3 py-2 text-sm text-foreground shadow-sm shadow-black/5 transition-shadow placeholder:text-muted-foreground/70 focus-visible:border-ring focus-visible:outline-none focus-visible:ring-[3px] focus-visible:ring-ring/20 disabled:cursor-not-allowed disabled:opacity-50",
          className,
        )}
        ref={ref}
        {...props}
      />
    );
  },
);
Textarea.displayName = "Textarea";

export { Textarea };
```

**2.3. ChatInput компонент из референса**

Создать `frontend/src/components/ui/chat-input.tsx`:

```typescript
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { useTextareaResize } from "@/hooks/use-textarea-resize";
import { ArrowUpIcon } from "lucide-react";
import type React from "react";
import { createContext, useContext } from "react";

// ... (полный код из референса 21st-ai-chat.md)
```

### 3. Создание Floating Chat компонентов

**3.1. FloatingChatButton**

Создать `frontend/src/components/FloatingChatButton.tsx`:

- Круглая кнопка с иконкой MessageCircle (lucide-react)
- Позиция: fixed, right-6, bottom-6
- Z-index: 50
- Badge с индикатором режима (обычный/администратор)
- onClick переключает состояние открытия чата

**3.2. FloatingChatWindow**

Создать `frontend/src/components/FloatingChatWindow.tsx`:

- Размер: w-96, h-[600px]
- Позиция: fixed, right-6, bottom-24
- Анимация появления/скрытия (transition)
- Структура:
  - Header: заголовок + переключатель режима + кнопка закрытия
  - Messages Area: список сообщений с автоскроллом
  - Input Area: ChatInput из референса
  - SQL Result (для админ режима)

**3.3. Логика чата**

Переиспользовать логику из `frontend/src/pages/Chat.tsx`:

- Управление состоянием сообщений
- Отправка сообщений через API
- Загрузка истории
- Переключение режимов (обычный/админ)
- Отображение SQL результатов

### 4. Интеграция в приложение

**4.1. Добавить FloatingChat в App.tsx**

Изменить `frontend/src/App.tsx`:

```typescript
import FloatingChat from './components/FloatingChat'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ... существующие роуты */}
      </Routes>
      <FloatingChat /> {/* Глобально для всех страниц */}
    </BrowserRouter>
  )
}
```

**4.2. Создать обертку FloatingChat**

Создать `frontend/src/components/FloatingChat.tsx`:

- Управляет состоянием isOpen
- Рендерит FloatingChatButton и FloatingChatWindow
- Содержит всю логику чата

### 5. Удаление старой страницы /chat

**5.1. Удалить файлы:**

- `frontend/src/pages/Chat.tsx`
- Роут `/chat` из `App.tsx`

**5.2. Обновить навигацию:**

- Удалить ссылку на Chat из `frontend/src/components/Sidebar.tsx`

**5.3. Удалить неиспользуемые компоненты:**

- `frontend/src/components/ChatInput.tsx` (заменен на chat-input из референса)
- `frontend/src/components/ChatMessage.tsx` (если не используется в других местах)

### 6. Стилизация и UX

**6.1. Адаптивный дизайн:**

- На мобильных: full screen overlay вместо floating окна
- Breakpoint: md (768px)

**6.2. Индикатор режима:**

- Badge на кнопке: "AI" (обычный) / "SQL" (администратор)
- Цвета: primary (обычный) / destructive (администратор)

**6.3. Поддержка темной/светлой темы:**

- Использовать существующий ThemeContext из `@/contexts/ThemeContext`
- Все компоненты должны использовать Tailwind CSS классы с поддержкой dark mode
- Цвета через CSS переменные: `bg-background`, `text-foreground`, `border-input`, etc.
- Компоненты из референса (chat-input, textarea) уже используют правильные классы
- Проверить работу в обоих режимах

**6.4. Анимации:**

- Fade in/out для окна чата
- Scale animation для кнопки при hover

### 7. Тестирование

**7.1. Функциональное тестирование:**

- Открытие/закрытие чата
- Отправка сообщений в обычном режиме
- Переключение на админ режим
- Выполнение Text2SQL запросов
- Очистка истории

**7.2. UI тестирование:**

- Адаптивность на разных экранах
- Работа темной/светлой темы
- Автоскролл при новых сообщениях
- Авто-ресайз textarea

## Итоговая структура файлов

```
frontend/src/
├── components/
│   ├── FloatingChat.tsx              # NEW: Обертка floating чата
│   ├── FloatingChatButton.tsx        # NEW: Кнопка в правом нижнем углу
│   ├── FloatingChatWindow.tsx        # NEW: Окно чата
│   ├── ui/
│   │   ├── chat-input.tsx           # NEW: Компонент из референса
│   │   ├── textarea.tsx             # NEW: Textarea из референса
│   ├── ChatMessage.tsx              # Переиспользуется
│   ├── SQLResultDisplay.tsx         # Переиспользуется
│   └── Sidebar.tsx                  # MODIFY: удалить ссылку на /chat
├── hooks/
│   └── use-textarea-resize.ts       # NEW: Hook из референса
├── pages/
│   ├── Dashboard.tsx                # Без изменений
│   └── Chat.tsx                     # DELETE
├── api/
│   └── chat.ts                      # Без изменений (API готов)
└── App.tsx                          # MODIFY: добавить FloatingChat, удалить роут /chat
```

## Критерии приемки

✅ Floating кнопка отображается в правом нижнем углу на всех страницах

✅ Клик по кнопке открывает/закрывает окно чата

✅ Окно чата имеет размер ~400x600px (desktop)

✅ На мобильных чат открывается на весь экран

✅ Работает обычный режим: отправка сообщений к LLM

✅ Работает админ режим: Text2SQL запросы

✅ Переключатель режимов в заголовке окна

✅ Индикатор текущего режима на кнопке

✅ Поддержка темной/светлой темы

✅ Автоскролл к последнему сообщению

✅ Авто-ресайз textarea при вводе

✅ Страница /chat удалена

✅ Старый ChatInput удален

✅ Навигация обновлена (нет ссылки на Chat)

### To-dos

- [x] Проверить и установить необходимые зависимости (если требуется)
- [x] Создать hook use-textarea-resize.ts из референса
- [x] Создать компонент ui/textarea.tsx из референса
- [x] Создать компонент ui/chat-input.tsx из референса
- [x] Создать FloatingChatButton с badge индикатором режима
- [x] Создать FloatingChatWindow с header, messages, input areas
- [x] Создать FloatingChat обертку с логикой чата
- [x] Интегрировать FloatingChat в App.tsx глобально
- [x] Удалить страницу Chat.tsx, роут /chat, старый ChatInput.tsx
- [x] Обновить Sidebar.tsx - удалить ссылку на Chat
- [x] Добавить адаптивный дизайн (mobile: full screen, desktop: floating)
- [x] Тестирование: обычный режим, админ режим, переключение, очистка истории

## Статус выполнения

**✅ Спринт 4 успешно завершен!**

Все задачи выполнены в полном объеме:

1. ✅ Создана полная структура Floating Chat с компонентами из референса
2. ✅ Интегрирован глобально в приложение (видно на всех страницах)
3. ✅ Реализованы оба режима работы: AI Assistant и SQL Assistant
4. ✅ Добавлена поддержка темной/светлой темы
5. ✅ Реализован адаптивный дизайн (mobile: full screen, desktop: floating window)
6. ✅ Удалена старая страница /chat и обновлена навигация
7. ✅ Обновлена документация (vision.md, README.md, frontend/README.md)
8. ✅ Проверено качество кода (ESLint, TypeScript, тесты)
9. ✅ Внесены изменения в репозиторий (commit: "feat: Спринт 4 - Реализация Floating AI-чата")

Дата завершения: 17 октября 2025