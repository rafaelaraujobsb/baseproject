SHELL := /bin/bash

ifeq ($(filter add-package add-dev-package,$(firstword $(MAKECMDGOALS))),$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

dependencies:
	sudo apt install -y make clang python3-dev libpq-dev

python-environment:
	source .venv/bin/activate

add-package:
	uv add $(RUN_ARGS)

add-dev-package:
	uv add --dev $(RUN_ARGS)

install-dev:
	UV_HTTP_TIMEOUT=600 uv sync --frozen

install-prod:
	UV_HTTP_TIMEOUT=600 uv sync --frozen --compile-bytecode --no-dev

run-dev:
	uv run uvicorn --host 0.0.0.0 src.main:app --reload

run:
	gunicorn -c gunicorn.conf.py src.main:app

run-compose:
	docker compose -f docker-compose.yaml up --build -d

stop-all:
	docker compose -f docker-compose.yaml stop

run-compose-dev:
	docker compose -f docker-compose.dev.yaml up --build -d

stop-all-dev:
	docker compose -f docker-compose.dev.yaml stop

test:
	uv run pytest -s --cov=src --cov-report=term-missing --cov-report=html tests

pre-commit:
	uv run ruff check
	uv run ruff format
	docker run --rm -i hadolint/hadolint < docker/Dockerfile
