CURRENT_DIRECTORY := $(shell pwd)


help:
	@echo "Docker Compose Help"
	@echo "-----------------------"
	@echo ""
	@echo "Run tests to ensure current state is good:"
	@echo "    make test"
	@echo ""
	@echo "If tests pass, add fixture data and start up the app:"
	@echo "    make begin"
	@echo ""
	@echo "Really, really start over:"
	@echo "    make clean"
	@echo ""
	@echo "See contents of Makefile for more targets."

first_run: build migrate cities_light start
begin: migrate start

start:
	@docker-compose up -d

prod-start:
	@docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d

stop:
	@docker-compose stop

status:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose rm --force
	@find . -name \*.pyc -delete

remove_volumes:
	@docker-compose down --volumes

build:
	@docker-compose build

test:
	@echo "Running test"
	@docker-compose run --rm web ./manage.py test

migrate:
	@echo "Running migrate"
	@docker-compose run --rm web ./manage.py migrate

cli:
	@docker-compose run --rm web bash

shell:
	@docker-compose run --rm web python ./manage.py shell_plus

tail:
	@docker-compose logs -f

cities_light:
	@echo "Running cities_light"
	@docker-compose run --rm web python ./manage.py cities_light

import_vacancies:
	@docker-compose run --rm web python ./manage.py import_vacancies --download latest

createsuperuser:
	@docker-compose run --rm web python ./manage.py createsuperuser


.PHONY: start stop status restart clean build test testwarn migrate fixtures cli tail
