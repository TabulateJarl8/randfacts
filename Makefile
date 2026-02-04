.PHONY: test test-cov lint format clean check-all

test:
	uv run pytest .

test-cov:
	 uv run pytest . --cov=randfacts --cov-report=term-missing --cov-report=xml

format:
	uv run ruff format .

lint:
	uv run ruff check .

clean:
	find . -type d -name "__pycache__" -exec rm -rfv "{}" +
	rm -rfv .mypy_cache .pytest_cache .ruff_cache dist
	rm -fv .coverage coverage.xml
	@command -v cargo >/dev/null 2>&1 && cargo clean --manifest-path tests/checkduplicates/Cargo.toml

check-all: test-cov lint
	uv run mypy .
	uv run ruff format . --check

