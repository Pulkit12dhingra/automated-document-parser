.PHONY: lint test requirements all

all: lint test

lint:
	uv run ruff check . --exclude "*.ipynb"

test:
	uv run pytest tests/

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