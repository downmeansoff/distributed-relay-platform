.PHONY: up down logs lint test deploy-staging deploy-prod

up:            ## Поднять локальный стенд
	docker compose up -d --build

down:          ## Остановить стенд
	docker compose down

logs:          ## Логи всех сервисов
	docker compose logs -f --tail=100

lint:          ## Линт Python и Bash
	ruff check backend monitoring
	shellcheck scripts/*.sh

test:          ## Юнит-тесты
	python -m pytest -q

deploy-staging: ## Выкатка на stage
	./scripts/deploy.sh staging

deploy-prod:   ## Выкатка в прод (rolling)
	./scripts/deploy.sh prod
