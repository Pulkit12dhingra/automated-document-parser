.PHONY: lint test requirements all build publish-test publish-pypi

all: lint test

lint:
	uv run ruff check . --exclude "*.ipynb"

test:
	uv run pytest test/

requirements:
	uv pip compile pyproject.toml --no-reuse-hashes --output-file=requirements.txt

format:
	uv run ruff format .

push: format requirements
	@bash -c '{ \
	set -e; \
	git add .; \
	read -p "Enter commit message: " msg; \
	echo "DEBUG: Entered message: [$${msg}]"; \
	if [ -z "$$(echo $${msg} | tr -d "[:space:]")" ]; then \
	  echo "Commit message cannot be blank or whitespace."; exit 1; \
	fi; \
	uv run pre-commit run --all-files || { \
	  echo "Pre-commit hooks failed. Files have been fixed. Please re-run make push."; \
	  exit 1; \
	}; \
	git add .; \
	git commit -m "$${msg}"; \
	git push; \
}'

build: format test
	@echo "Building package..."
	rm -rf dist/
	uv run python -m build
	@echo "Checking package..."
	uv run twine check dist/*
	@echo "Build complete! Distribution files in dist/"

publish-test: build
	@echo "Uploading to TestPyPI..."
	uv run twine upload --repository testpypi dist/* --username __token__ --password "$${PYPI_API_TOKEN}"
	@echo "Published to TestPyPI!"
	@echo "Install with: pip install --index-url https://test.pypi.org/simple/ langchain-document-parser"

publish-pypi: build
	@echo "WARNING: Publishing to production PyPI!"
	@read -p "Are you sure? (yes/N): " confirm; \
	if [ "$${confirm}" != "yes" ]; then \
	  echo "Publish cancelled."; exit 1; \
	fi
	@echo "Uploading to PyPI..."
	uv run twine upload dist/* --username __token__ --password "$${PYPI_API_TOKEN}"
	@echo "Published to PyPI!"
	@echo "Install with: pip install langchain-document-parser"

