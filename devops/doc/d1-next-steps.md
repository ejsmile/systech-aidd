# Спринт D1: Следующие шаги

**Статус:** ✅ Реализация завершена  
**Дата:** 2025-10-18

## 🎯 Что было сделано

✅ Создана полная документация по GitHub Actions  
✅ Настроен GitHub Actions workflow для автоматической сборки  
✅ Создан docker-compose.registry.yml для использования образов из registry  
✅ Обновлен README.md с badge и инструкциями  
✅ Обновлен DevOps roadmap  

## 📋 Что нужно сделать для запуска CI/CD

### Шаг 1: Commit и Push изменений

```bash
# Проверить статус
git status

# Добавить все изменения
git add .

# Commit
git commit -m "feat(devops): add GitHub Actions CI/CD pipeline for D1 sprint

- Add GitHub Actions workflow for building and publishing Docker images
- Add docker-compose.registry.yml for using images from ghcr.io
- Add comprehensive GitHub Actions documentation
- Update README.md with build badge and registry usage instructions
- Update DevOps roadmap with D1 completion status
- Add detailed D1 implementation plan

Closes: Sprint D1 - Build & Publish"

# Push в текущую ветку (feat/ci)
git push origin feat/ci
```

### Шаг 2: Создать Pull Request на main

1. Перейти на GitHub: https://github.com/ejsmile/systech-aidd/pulls
2. Нажать "New Pull Request"
3. Выбрать: base: `main` ← compare: `feat/ci`
4. Заполнить PR:
   - **Title:** `feat(devops): Sprint D1 - Build & Publish CI/CD`
   - **Description:**
     ```markdown
     ## Спринт D1: Build & Publish
     
     Автоматическая сборка и публикация Docker образов в GitHub Container Registry.
     
     ### Что добавлено:
     - ✅ GitHub Actions workflow (.github/workflows/build.yml)
     - ✅ Matrix strategy для параллельной сборки 3 образов
     - ✅ Кэширование Docker layers для ускорения
     - ✅ Условная публикация (только main ветка)
     - ✅ docker-compose.registry.yml для использования образов из ghcr.io
     - ✅ Полная документация по GitHub Actions
     - ✅ README обновлен (badge + инструкции)
     
     ### Как тестировать:
     1. Проверить что workflow запустился
     2. Проверить что все 3 образа собрались успешно
     3. После merge в main - проверить публикацию в ghcr.io
     
     ### Документация:
     - [GitHub Actions Guide](devops/doc/github-actions-guide.md)
     - [D1 Implementation Plan](devops/doc/plans/d1-build-publish.md)
     - [DevOps Roadmap](devops/doc/devops-roadmap.md)
     ```

5. Нажать "Create Pull Request"

### Шаг 3: Проверка workflow в PR

После создания PR:

1. Перейти во вкладку **Actions**: https://github.com/ejsmile/systech-aidd/actions
2. Найти workflow **"Build and Publish"** для вашего PR
3. Проверить:
   - ✅ Workflow запустился автоматически
   - ✅ Три параллельных job'а: build (bot), build (api), build (frontend)
   - ✅ Все job'ы завершились успешно (зеленая галочка)
   - ⚠️ Образы собрались, но **НЕ опубликовались** (это нормально для PR)

**Что делать если workflow failed:**
- Открыть failed job
- Посмотреть логи (красные строки)
- Исправить проблему
- Push исправлений → workflow перезапустится автоматически

### Шаг 4: Merge PR в main

После успешной проверки:

1. В PR нажать **"Merge pull request"**
2. Выбрать **"Squash and merge"** (опционально)
3. Подтвердить merge
4. Удалить feature ветку (опционально)

### Шаг 5: Проверка публикации образов

После merge в main:

1. Перейти в **Actions**: https://github.com/ejsmile/systech-aidd/actions
2. Найти workflow для main ветки
3. Дождаться завершения (обычно 7-10 минут)
4. Перейти в **Packages**: https://github.com/ejsmile?tab=packages
5. Убедиться что появились 3 пакета:
   - `systech-aidd-bot`
   - `systech-aidd-api`
   - `systech-aidd-frontend`

### Шаг 6: Настройка публичного доступа

**Для каждого образа (bot, api, frontend):**

1. В списке Packages кликнуть на образ
2. Справа внизу найти **"Package settings"**
3. Прокрутить вниз до **"Danger Zone"**
4. Найти **"Change package visibility"**
5. Нажать **"Change visibility"**
6. Выбрать **"Public"**
7. Ввести имя пакета для подтверждения
8. Нажать **"I understand, change package visibility"**

**Повторить для всех трех образов!**

### Шаг 7: Проверка доступности образов

```bash
# Должны скачаться БЕЗ авторизации (если visibility = public)
docker pull ghcr.io/ejsmile/systech-aidd-bot:latest
docker pull ghcr.io/ejsmile/systech-aidd-api:latest
docker pull ghcr.io/ejsmile/systech-aidd-frontend:latest

# Проверить что образы скачались
docker images | grep systech-aidd
```

**Ожидаемый результат:**
```
ghcr.io/ejsmile/systech-aidd-bot       latest   abc123   5 minutes ago   200MB
ghcr.io/ejsmile/systech-aidd-api       latest   abc123   5 minutes ago   200MB
ghcr.io/ejsmile/systech-aidd-frontend  latest   def456   5 minutes ago   300MB
```

### Шаг 8: Запуск через docker-compose.registry.yml

```bash
# Убедиться что .env файл существует
cp sample.env .env
# Отредактировать токены

# Запустить через образы из registry
docker-compose -f docker-compose.registry.yml up -d

# Проверить статус
docker-compose -f docker-compose.registry.yml ps

# Должны быть запущены:
# - systech-aidd-postgres (running)
# - systech-aidd-bot (running)
# - systech-aidd-api (running)
# - systech-aidd-frontend (running)
```

**Проверка работоспособности:**
- API: http://localhost:8000/docs (должна открыться Swagger документация)
- Frontend: http://localhost:5173 (должна открыться страница дашборда)
- Telegram Bot: отправить `/start` боту - должен ответить

### Шаг 9: Проверка badge в README

1. Перейти на главную страницу репозитория: https://github.com/ejsmile/systech-aidd
2. В README.md должен появиться badge **"Build Status"** со статусом **"passing"** (зеленый)
3. Кликнув на badge можно перейти к Actions

## 📊 Критерии успешного завершения

- ✅ PR создан и workflow прошел успешно
- ✅ Merge в main выполнен
- ✅ Все 3 образа опубликованы в ghcr.io
- ✅ Visibility образов = Public
- ✅ Образы скачиваются без авторизации
- ✅ docker-compose.registry.yml запускает все сервисы
- ✅ Badge "Build Status" показывает "passing"
- ✅ API, Frontend и Bot работают корректно

## 🔧 Troubleshooting

### Проблема: Workflow не запускается

**Решение:**
- Проверить что файл `.github/workflows/build.yml` существует
- Проверить синтаксис YAML (spaces, not tabs)
- Проверить что push выполнен в GitHub

### Проблема: Build failed - Dockerfile not found

**Решение:**
```yaml
# В build.yml проверить пути:
file: ${{ matrix.context }}/${{ matrix.dockerfile }}

# Для bot/api должно быть: ./Dockerfile.backend
# Для frontend должно быть: ./frontend/Dockerfile
```

### Проблема: Permission denied при публикации

**Решение:**
- Проверить что в workflow есть: `permissions: packages: write`
- Проверить что `GITHUB_TOKEN` не expired

### Проблема: Образы не публикуются

**Причина:** публикация происходит только при push в `main`

**Решение:**
- PR только собирают образы (это нормально)
- После merge в main образы должны опубликоваться

### Проблема: Cannot pull image - unauthorized

**Причина:** образы private по умолчанию

**Решение:** изменить visibility на Public (см. Шаг 6)

### Проблема: docker-compose.registry.yml не запускается

**Проверить:**
```bash
# 1. Образы существуют
docker pull ghcr.io/ejsmile/systech-aidd-bot:latest

# 2. .env файл существует и содержит токены
cat .env | grep TOKEN

# 3. Postgres порт не занят
lsof -i :5433

# 4. Логи сервисов
docker-compose -f docker-compose.registry.yml logs
```

## 📚 Полезные команды

```bash
# Проверить статус workflow
gh run list --workflow=build.yml

# Посмотреть логи последнего run
gh run view --log

# Список образов в registry
gh api /user/packages?package_type=container

# Pull конкретного commit
docker pull ghcr.io/ejsmile/systech-aidd-bot:sha-abc1234

# Обновить образы до latest
docker-compose -f docker-compose.registry.yml pull
docker-compose -f docker-compose.registry.yml up -d

# Очистка старых образов
docker image prune -a
```

## 🎓 Дополнительная информация

- **GitHub Actions документация:** [devops/doc/github-actions-guide.md](github-actions-guide.md)
- **Детальный план D1:** [devops/doc/plans/d1-build-publish.md](plans/d1-build-publish.md)
- **DevOps roadmap:** [devops/doc/devops-roadmap.md](devops-roadmap.md)
- **GitHub Actions официальная документация:** https://docs.github.com/en/actions

## 🚀 Следующие спринты

### D2: Развертывание на сервер (Manual Deploy)
- Пошаговая инструкция деплоя
- SSH настройка
- Production конфигурация

### D3: Auto Deploy
- Автоматический деплой через GitHub Actions
- One-click deployment

---

**Готово к тестированию!** 🎉

Следуйте шагам выше для проверки работы CI/CD pipeline.

