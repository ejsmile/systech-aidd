# GitHub Actions: Руководство по CI/CD

> Практическое руководство по использованию GitHub Actions для автоматизации сборки и публикации Docker образов

## Содержание

- [Основы GitHub Actions](#основы-github-actions)
- [Триггеры событий](#триггеры-событий)
- [Работа с Pull Requests](#работа-с-pull-requests)
- [Matrix Strategy](#matrix-strategy)
- [GitHub Container Registry](#github-container-registry)
- [Visibility образов](#visibility-образов)
- [Permissions и безопасность](#permissions-и-безопасность)

---

## Основы GitHub Actions

### Что такое GitHub Actions?

**GitHub Actions** — это платформа CI/CD, встроенная в GitHub, которая позволяет автоматизировать процессы разработки: сборку, тестирование, деплой и другие задачи.

### Ключевые концепции

#### Workflow (Рабочий процесс)
- YAML файл в директории `.github/workflows/`
- Описывает автоматизированный процесс
- Запускается при определенных событиях (push, PR, schedule и т.д.)

**Пример:**
```yaml
name: Build and Publish
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t myapp .
```

#### Job (Задача)
- Набор шагов (steps), выполняемых на одном runner
- Несколько jobs могут выполняться параллельно
- Jobs могут зависеть друг от друга через `needs`

#### Step (Шаг)
- Отдельное действие внутри job
- Может быть командой shell или использованием готового action
- Выполняются последовательно

#### Runner (Исполнитель)
- Виртуальная машина, на которой выполняется workflow
- GitHub предоставляет runners: `ubuntu-latest`, `windows-latest`, `macos-latest`
- Можно использовать self-hosted runners

### Структура проекта с GitHub Actions

```
.github/
└── workflows/
    ├── build.yml       # Сборка и публикация образов
    ├── test.yml        # Запуск тестов (будущее)
    └── deploy.yml      # Деплой на сервер (будущее)
```

---

## Триггеры событий

Триггеры определяют, когда запускается workflow.

### Push (Отправка кода)

Запуск при push в определенные ветки:

```yaml
on:
  push:
    branches:
      - main           # Только main
      - 'feature/**'   # Все feature ветки
      - '**'           # Все ветки
```

Запуск при изменении определенных файлов:

```yaml
on:
  push:
    paths:
      - 'src/**'       # Только при изменении src/
      - 'Dockerfile.*' # Только при изменении Dockerfile
```

### Pull Request

Запуск при создании/обновлении PR:

```yaml
on:
  pull_request:
    branches:
      - main           # PR только на main
    types:
      - opened         # При создании PR
      - synchronize    # При push в PR
      - reopened       # При reopened PR
```

### Workflow Dispatch (Ручной запуск)

Запуск вручную через GitHub UI:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

### Комбинирование триггеров

```yaml
on:
  push:
    branches: ['**']      # Push в любую ветку
  pull_request:
    branches: [main]      # PR только на main
  workflow_dispatch:      # Ручной запуск
```

---

## Работа с Pull Requests

### Зачем CI в Pull Requests?

Pull Request — это предложение изменений перед merge в основную ветку. CI в PR позволяет:

1. **Проверить сборку** — убедиться, что код компилируется
2. **Запустить тесты** — проверить, что изменения не ломают функциональность
3. **Проверить качество** — линтинг, форматирование, type checking
4. **Дать feedback** — автоматические комментарии о проблемах

### Workflow для Pull Requests

**Типичный сценарий:**

```yaml
name: PR Check
on:
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build Docker images
        run: docker-compose build
      
      - name: Run tests
        run: docker-compose run --rm api pytest
```

### Условная логика для PR

Разное поведение для PR и main:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build image
        run: docker build -t myapp .
      
      # Публикация только для main, не для PR
      - name: Push to registry
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        run: docker push myapp
```

### Защита ветки через Branch Protection

В настройках репозитория (`Settings → Branches`):
- ✅ Require status checks before merging
- ✅ Require branches to be up to date
- Выбрать workflows, которые должны пройти успешно

**Результат:** merge в main возможен только после успешного прохождения CI.

---

## Matrix Strategy

**Matrix Strategy** позволяет запускать один job с разными параметрами параллельно.

### Простой пример: сборка нескольких образов

```yaml
jobs:
  build:
    strategy:
      matrix:
        service: [bot, api, frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build ${{ matrix.service }}
        run: docker build -t ${{ matrix.service }} .
```

**Результат:** запустятся 3 параллельных job'а:
- build (bot)
- build (api)
- build (frontend)

### Расширенная matrix с несколькими параметрами

```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest]
    python: ['3.10', '3.11', '3.12']
```

**Результат:** 6 комбинаций (2 OS × 3 версии Python)

### Matrix с include/exclude

```yaml
strategy:
  matrix:
    service: [bot, api, frontend]
    include:
      - service: bot
        dockerfile: Dockerfile.backend
        context: .
      - service: api
        dockerfile: Dockerfile.backend
        context: .
      - service: frontend
        dockerfile: Dockerfile
        context: ./frontend
```

**Доступ к переменным:**
```yaml
- name: Build ${{ matrix.service }}
  run: |
    docker build \
      -f ${{ matrix.dockerfile }} \
      -t ${{ matrix.service }} \
      ${{ matrix.context }}
```

### Преимущества Matrix Strategy

- ✅ **Параллелизм** — все комбинации выполняются одновременно
- ✅ **DRY** — не нужно дублировать код для каждого сервиса
- ✅ **Масштабируемость** — легко добавить новый сервис
- ✅ **Единообразие** — все сервисы собираются одинаково

---

## GitHub Container Registry

**GitHub Container Registry (ghcr.io)** — бесплатный Docker registry от GitHub.

### Преимущества ghcr.io

- ✅ Бесплатный для публичных репозиториев
- ✅ Интеграция с GitHub (авторизация через `GITHUB_TOKEN`)
- ✅ Unlimited storage для публичных образов
- ✅ Automatic cleanup policies
- ✅ Поддержка OCI artifacts

### Формат образов

```
ghcr.io/<username>/<image-name>:<tag>
```

**Примеры:**
```
ghcr.io/ejsmile/systech-aidd-bot:latest
ghcr.io/ejsmile/systech-aidd-bot:sha-abc1234
ghcr.io/ejsmile/systech-aidd-api:v1.0.0
```

### Авторизация в ghcr.io

В GitHub Actions используется встроенный `GITHUB_TOKEN`:

```yaml
- name: Login to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**Локальная авторизация:**
```bash
# Создать Personal Access Token в GitHub Settings → Developer settings
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Публикация образов

```yaml
- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: |
      ghcr.io/ejsmile/systech-aidd-bot:latest
      ghcr.io/ejsmile/systech-aidd-bot:sha-${{ github.sha }}
```

### Pull образов

**Публичные образы** (без авторизации):
```bash
docker pull ghcr.io/ejsmile/systech-aidd-bot:latest
```

**Приватные образы** (с авторизацией):
```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker pull ghcr.io/ejsmile/systech-aidd-bot:latest
```

---

## Visibility образов

По умолчанию образы в ghcr.io **приватные** (private). Для публичного доступа нужно изменить visibility.

### Public vs Private

| Параметр | Public | Private |
|----------|--------|---------|
| Доступ без авторизации | ✅ Да | ❌ Нет |
| Storage quota | ♾️ Unlimited | Limited |
| Подходит для open source | ✅ Да | ❌ Нет |
| Безопасность | Все видят | Только с доступом |

### Изменение visibility через GitHub UI

**Шаги:**

1. Перейти на страницу репозитория GitHub
2. Справа найти секцию **Packages** → кликнуть на образ
3. В правом меню → **Package settings**
4. Внизу страницы → **Change visibility**
5. Выбрать **Public** → подтвердить

**Скриншот пути:**
```
GitHub → Repo → Packages → [Package] → Settings → Change visibility → Public
```

### Автоматическое изменение visibility (опционально)

Можно использовать GitHub CLI в workflow:

```yaml
- name: Make package public
  if: github.ref == 'refs/heads/main'
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    gh api \
      --method PATCH \
      -H "Accept: application/vnd.github+json" \
      /user/packages/container/systech-aidd-bot/versions/latest \
      -f visibility='public'
```

**Примечание:** для MVP проще настроить вручную один раз.

### Проверка доступности

**Публичный образ:**
```bash
# Должен скачаться без авторизации
docker pull ghcr.io/ejsmile/systech-aidd-bot:latest
```

---

## Permissions и безопасность

### GITHUB_TOKEN

`GITHUB_TOKEN` — это автоматически созданный токен для каждого workflow.

**Возможности:**
- Чтение кода репозитория
- Публикация образов в ghcr.io
- Создание issues, комментариев
- И другие операции (зависит от permissions)

### Настройка permissions в workflow

По умолчанию `GITHUB_TOKEN` имеет read-only доступ. Для публикации образов нужны права записи:

```yaml
name: Build and Publish

on:
  push:
    branches: ['**']

permissions:
  contents: read      # Чтение кода
  packages: write     # Публикация в ghcr.io

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Login to ghcr.io
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
```

### Безопасность secrets

**Не используйте:**
- ❌ Hardcoded токены в коде
- ❌ Токены в commit history
- ❌ `.env` файлы в git

**Используйте:**
- ✅ `secrets.GITHUB_TOKEN` для ghcr.io
- ✅ Repository secrets для других токенов (`Settings → Secrets`)
- ✅ Environment secrets для production

**Добавление секретов:**
```
Repo → Settings → Secrets and variables → Actions → New repository secret
```

### Best practices безопасности

1. **Минимальные permissions** — давайте только необходимые права
2. **Условная публикация** — публикуйте образы только из main
3. **Readonly для PR** — PR не должны иметь write access
4. **Rotate tokens** — периодически обновляйте Personal Access Tokens
5. **Review dependencies** — проверяйте используемые actions

---

## Полезные ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry Guide](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)

---

## Практический пример: наш workflow

Полный workflow для проекта systech-aidd:

```yaml
name: Build and Publish

on:
  push:
    branches: ['**']
  pull_request:
    branches: [main]

permissions:
  contents: read
  packages: write

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - service: bot
            dockerfile: Dockerfile.backend
            context: .
          - service: api
            dockerfile: Dockerfile.backend
            context: .
          - service: frontend
            dockerfile: Dockerfile
            context: ./frontend
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to GitHub Container Registry
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/ejsmile/systech-aidd-${{ matrix.service }}
          tags: |
            type=raw,value=latest
            type=sha,prefix=sha-
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: ${{ matrix.context }}
          file: ${{ matrix.context }}/${{ matrix.dockerfile }}
          push: ${{ github.event_name == 'push' && github.ref == 'refs/heads/main' }}
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**Что происходит:**
1. ✅ Workflow запускается при push в любую ветку и PR на main
2. ✅ Параллельно собирается 3 образа (bot, api, frontend)
3. ✅ Используется кэширование для ускорения сборки
4. ✅ Образы публикуются в ghcr.io только при push в main
5. ✅ PR только проверяют сборку без публикации

---

**Готово!** Теперь у вас есть полное понимание GitHub Actions для автоматизации CI/CD.

