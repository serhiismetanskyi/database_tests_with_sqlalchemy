default: help

help: ## display available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

up: ## up project
	docker-compose up --build

start: ## start project
	docker-compose start

stop: ## stop project
	docker-compose stop

down: ## down project
	docker-compose down --remove-orphans

restart: ## restart project
	docker-compose restart

install-deps: ## install dependencies
	poetry install --with dev,test --no-root

lint: install-deps ## check code
	black src && black tests && isort src && isort tests && pylint src && pylint tests && mypy src && mypy tests
