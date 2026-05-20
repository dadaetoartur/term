PYTHON_VERSION := python3.12

PYTEST_ARGS := --doctest-modules --cov=service
PYTEST_REPORT_ARGS :=  --cov-report=xml:coverage.xml

DEPLOY_DIR := docker
DOCKER_CONTAINER_SERVICE_NAME := term-backend

.PHONY: install
install:
	@poetry env use $(PYTHON_VERSION)
	@poetry install
	@poetry run pre-commit install

.PHONY: docker.service.compose.run
docker.service.compose.run:
	@cd $(DEPLOY_DIR) && docker-compose -f docker-compose.local.yml up --build

.PHONY: test.pytest
test.pytest:
	@pytest $(PYTEST_ARGS) -- tests

.PHONY: test.coverage
test.coverage:
	@pytest $(PYTEST_ARGS) $(PYTEST_REPORT_ARGS) -- tests

.PHONY: pre-commit-all
pre-commit-all:
	@pre-commit run --all-files

.PHONY: alembic.remote.upgrade
alembic.remote.upgrade:
	@docker exec -it $(DOCKER_CONTAINER_SERVICE_NAME) sh -c "alembic upgrade head"

.PHONY: alembic.remote.downgrade
alembic.remote.downgrade:
	@docker exec -it $(DOCKER_CONTAINER_SERVICE_NAME) sh -c "alembic downgrade -1"

.PHONY: alembic.remote.revision
alembic.remote.revision:
	@docker exec -it $(DOCKER_CONTAINER_SERVICE_NAME) sh -c "alembic revision --autogenerate -m 'init service'"
	@docker cp $(DOCKER_CONTAINER_SERVICE_NAME):/app/alembic/versions/ ./alembic/
