.PHONY: install install-dev run dev run-api test-api clean format lint typecheck quality test test-cov db-up db-down db-migrate db-revision db-reset restart frontend-install frontend-dev frontend-build frontend-preview frontend-lint frontend-format frontend-test frontend-quality quality-all

install:
	uv pip install -e .

install-dev:
	uv pip install -e ".[dev]"

run:
	uv run python -m src.main

dev:
	LOG_LEVEL=DEBUG uv run python -m src.main

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

format:
	uv run ruff format .

lint:
	uv run ruff check . --fix

typecheck:
	uv run mypy src/

quality: format lint typecheck
	@echo "✅ Backend code quality checks passed"

test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

test-docker:
	docker compose -f docker-compose.test.yml run --rm test-backend

test-docker-build:
	docker compose -f docker-compose.test.yml build test-backend

# Database commands
db-up:
	docker compose up -d postgres
	@echo "⏳ Waiting for PostgreSQL to be ready..."
	@sleep 3
	@echo "✅ PostgreSQL is ready"

db-down:
	docker compose down

db-migrate:
	uv run alembic upgrade head

db-revision:
	uv run alembic revision --autogenerate -m "$(m)"

db-reset:
	docker compose down -v
	docker compose up -d postgres
	@echo "⏳ Waiting for PostgreSQL to be ready..."
	@sleep 3
	uv run alembic upgrade head
	@echo "✅ Database reset complete"

restart:
	@echo "🔄 Restarting bot..."
	@pkill -f "python -m src.main" || true
	@sleep 1
	uv run python -m src.main

# API commands
run-api:
	uv run python -m src.api.main

test-api:
	uv run pytest tests/test_api_endpoints.py -v

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

frontend-format:
	cd frontend && npm run format

frontend-test:
	cd frontend && npm run test:run

frontend-quality: frontend-format frontend-lint
	@echo "✅ Frontend code quality checks passed"

quality-all: quality frontend-quality
	@echo "✅ All code quality checks passed (Backend + Frontend)"

