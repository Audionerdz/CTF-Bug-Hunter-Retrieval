.PHONY: help install test lint format coverage clean docker build-docker run-docker

help:
	@echo "RAG-Graph Development Commands"
	@echo "=============================="
	@echo "make install          Install dependencies"
	@echo "make test            Run all tests"
	@echo "make smoke-test      Run smoke tests only"
	@echo "make lint            Run linting checks"
	@echo "make format          Format code with black"
	@echo "make type-check      Run type checking"
	@echo "make coverage        Generate coverage report"
	@echo "make clean           Clean build artifacts"
	@echo "make docker-build    Build Docker image"
	@echo "make docker-run      Run Docker container"
	@echo ""

install:
	pip install -r rag_graph/requirements_rag_graph.txt
	pip install black flake8 mypy pytest-cov

test:
	pytest rag_graph/tests/ -v

smoke-test:
	python rag_graph/tests/smoke_tests.py

lint:
	flake8 rag_graph/ --max-line-length=100 --count

format:
	black rag_graph/

type-check:
	mypy rag_graph/ --ignore-missing-imports

coverage:
	pytest rag_graph/tests/ --cov=rag_graph --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/

docker-build:
	docker build -f rag_graph/Dockerfile.rag-graph -t rag-graph:latest .

docker-run:
	docker run -p 8001:8001 rag-graph:latest

all: clean install lint format test coverage
	@echo "All checks passed!"
