.PHONY: install update clean dev load assets optimize setup

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "setup		set up the original test project"
	@echo "reload_dev	For debugging purposes, make a simple Docker reload"
	@echo "*_dev		More dev related commands, look in code"


setup:
	docker-compose down -v
	docker-compose rm -f
	docker volume prune -f
	docker-compose build --no-cache && docker-compose up -d

reload_dev:
	docker-compose down -v
	docker-compose build && docker-compose up -d

# Makefile

up:
	docker-compose up --build

down:
	docker-compose down -v

restart: down up -d

logs:
	docker-compose logs -f

ps:
	docker-compose ps

bash:
	docker exec -it fastapi-app bash

mysql:
	docker exec -it fastapi-db mysql -u fastapi -pfastapi filters_db

seed:
	docker exec -i fastapi-db mysql -u fastapi -pfastapi filters_db < docker-entrypoint-initdb.d/mysql-init.sql
