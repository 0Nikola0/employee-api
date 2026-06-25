IMAGE_NAME=employees-api
CONTAINER_NAME=employees-api

run:
	docker compose up --build

test:
	docker compose run --rm employees_api pytest

stop:
	docker compose down