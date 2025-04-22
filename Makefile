.PHONY: test test-simple clean install dev

# Default target
all: install

# Install dependencies
install:
	./scripts/uv.sh install

# Install development dependencies
dev:
	./scripts/uv.sh dev

# Run all tests
test:
	pytest tests/

# Run simple test
test-simple:
	pytest tests/test_simple.py -v

# Clean up
clean:
	./scripts/uv.sh clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".tox" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

# Help command
help:
	@echo "Available commands:"
	@echo "  make install    - Install main dependencies"
	@echo "  make dev       - Install development dependencies"
	@echo "  make test      - Run all tests"
	@echo "  make test-simple - Run simple test"
	@echo "  make clean     - Clean up project"
	@echo "  make help      - Show this help message" 