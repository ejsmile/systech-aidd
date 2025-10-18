FROM node:20-alpine

WORKDIR /app

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование остальных файлов проекта
COPY . .

# Открытие порта Vite dev сервера
EXPOSE 5173

# Запуск dev сервера с доступом извне контейнера
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

