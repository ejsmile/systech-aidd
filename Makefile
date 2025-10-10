.PHONY: install run dev clean

install:
	uv pip install -e .

run:
	uv run python -m src.main

dev:
	LOG_LEVEL=DEBUG uv run python -m src.main

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

