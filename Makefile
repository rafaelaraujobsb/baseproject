SHELL := /bin/bash

# adicionar o add-dev-package
ifeq ($(filter add-package add-dev-package,$(firstword $(MAKECMDGOALS))),$(firstword $(MAKECMDGOALS)))
  # use the rest as arguments for "good"
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # ...and turn them into do-nothing targets
  $(eval $(RUN_ARGS):;@:)
endif

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

python-environment:
	source .venv/bin/activate

add-package:
	uv add $(RUN_ARGS)

add-dev-package:
	uv add --dev $(RUN_ARGS)

install-dev:
	uv sync --frozen

install-prod:
	uv sync --frozen --compile-bytecode --no-dev

run-dev:
	LOG_LEVEL=DEBUG uv run uvicorn --host 0.0.0.0 src.main:app --reload

run:
	LOG_LEVEL=INFO uv run gunicorn -c gunicorn.conf.py src.main:app

run-compose:
	docker compose -f docker-compose.yaml up --build -d

stop-all:
	docker compose -f docker-compose.yaml stop

run-compose-dev:
	docker compose -f docker-compose.dev.yaml up --build -d

stop-all-dev:
	docker compose -f docker-compose.dev.yaml stop

test:
	uv run pytest --cov=src --cov-report=term-missing --cov-report=html tests

pre-commit:
	uv run ruff check --select I --fix
	uv run ruff format
