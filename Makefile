IMAGE_NAME=employees-api
CONTAINER_NAME=employees-api

run:
	docker compose up --build

test:
	docker compose run --rm employees_api pytest

populate:
	docker compose run --rm employees_api python src/scripts/populate_db.py

import:
	docker compose run --rm employees_api python src/scripts/import_employees.py

stop:
	docker compose down