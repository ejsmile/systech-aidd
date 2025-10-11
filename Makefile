.PHONY: install install-dev run dev clean format lint typecheck quality

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
	@echo "✅ Code quality checks passed"

