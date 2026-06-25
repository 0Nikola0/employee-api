Project structure
---
Project is firstly split in 2 main folders: src/ and tests/. \
In src/ is the main source code, and in tests/ are the tests for that code. \
The source code is organized mainly in 4 subdirectories: models, repository, service and router. \
Models contains the database, request and response data models. \
Repository is for the connection to the database. \
Service holds the business logic and interacts between the router and repository layer. \
The router is for the exposed API endpoints. \
Additionally the project contains a folder with extra code that can be run in standalone in the scripts/ folder. \
From here you can seed the db / fetch data from an external API. \
These two scripts can be configured to run automatically on app startup with an environemntal variables. \

Needs
---
- Python 3.11+
- Docker (if you want to run it in container)

Quickstart (three ways)
---

### 1. Venv

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run the app:

```bash
python -m src
```

### 2. Docker and docker-compose

Build and run with docker-compose

```bash
docker compose up --build
```


### 3. Makefile targets

Makefile is configured to call the docker commands in the background

```bash
make run
make test
make stop
```

.env and startup scripts
---
Create a `.env` file (copy from `.env.example` if present) and set any required variables. Two environment flags control automatic startup behavior:

- `FETCH_ON_START=1` — when set to `1`, the app will attempt to fetch employees from the external API on startup.
- `SEED_DB=1` — when set to `1`, the app will seed the database with example data on startup.

Running the scripts manually
---
You can run scripts directly from the project root (with an activated venv or inside the container):

1. Venv
```bash
python src/scripts/import_employees.py
python src/scripts/populate_db.py
```

2. Docker
```bash
docker compose run --rm employees_api python src/scripts/import_employees.py
docker compose run --rm employees_api python src/scripts/populate_db.py
```

3. Make
```bash
make import
make populate
```


Testing
---
Run the test suite locally with `pytest`:

```bash
pytest -q
```

Or run the tests with Docker Compose 

```bash
docker compose run --rm employees_api pytest -q
```

Or with Makefile:

```bash
make test
```

Swagger docs
---
Once the app is running, open the API documentation at:

http://localhost:8000/docs
