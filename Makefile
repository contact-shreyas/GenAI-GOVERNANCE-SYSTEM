DOCKER_COMPOSE ?= docker compose

.PHONY: build up down logs ps backend-migrate backend-reset sanity frontend-lock frontend-test

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up -d

logs:
	$(DOCKER_COMPOSE) logs -f

ps:
	$(DOCKER_COMPOSE) ps

down:
	$(DOCKER_COMPOSE) down

backend-migrate:
	$(DOCKER_COMPOSE) run --rm backend alembic -c /app/alembic.ini upgrade head

backend-reset:
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) up -d postgres redis
	$(DOCKER_COMPOSE) run --rm backend alembic -c /app/alembic.ini upgrade head

sanity:
	python backend/scripts/sanity_check.py

frontend-lock:
	cd frontend && corepack enable && corepack prepare pnpm@8.15.4 --activate && pnpm install --lockfile-only --ignore-scripts

frontend-test:
	cd frontend && pnpm test
