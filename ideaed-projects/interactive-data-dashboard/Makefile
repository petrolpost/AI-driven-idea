.PHONY: help install install-dev test test-cov lint format type-check clean run dev build docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo "  test         - Run tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo "  lint         - Run linting (ruff)"
	@echo "  format       - Format code (black)"
	@echo "  type-check   - Run type checking (mypy)"
	@echo "  clean        - Clean build artifacts"
	@echo "  run          - Run the dashboard application"
	@echo "  dev          - Run in development mode with auto-reload"
	@echo "  build        - Build the package"
	@echo "  docs         - Generate documentation"

# Installation
install:
	uv sync

install-dev:
	uv sync --extra dev

# Testing
test:
	uv run pytest

test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

test-watch:
	uv run pytest-watch

# Code quality
lint:
	uv run ruff check src/ tests/

lint-fix:
	uv run ruff check --fix src/ tests/

format:
	uv run black src/ tests/

format-check:
	uv run black --check src/ tests/

type-check:
	uv run mypy src/

# Combined quality checks
check: format-check lint type-check test

fix: format lint-fix

# Development
run:
	uv run streamlit run src/interactive_data_dashboard/main.py

dev:
	uv run streamlit run src/interactive_data_dashboard/main.py --server.runOnSave true --server.fileWatcherType poll

dev-debug:
	uv run streamlit run src/interactive_data_dashboard/main.py --server.runOnSave true --server.fileWatcherType poll --logger.level debug

# Build and distribution
build:
	uv build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "API documentation available at: http://localhost:8501/docs"

# Environment setup
setup-pre-commit:
	uv run pre-commit install

setup-dev: install-dev setup-pre-commit
	@echo "Development environment setup complete!"

# Performance testing
test-performance:
	uv run pytest tests/test_performance.py -v

# Security scanning
security-check:
	uv run safety check

# Docker commands (if using Docker)
docker-build:
	docker build -t interactive-data-dashboard .

docker-run:
	docker run -p 8501:8501 interactive-data-dashboard

# Deployment helpers
deploy-check: check test-cov
	@echo "Ready for deployment!"

# Database/cache cleanup (if applicable)
clean-cache:
	rm -rf .streamlit/
	rm -rf ~/.streamlit/

# Version management
version-patch:
	uv run bump2version patch

version-minor:
	uv run bump2version minor

version-major:
	uv run bump2version major

# Quick development workflow
quick-check: format lint test
	@echo "Quick check completed!"

# Full CI/CD simulation
ci: install-dev check test-cov
	@echo "CI pipeline simulation completed!"