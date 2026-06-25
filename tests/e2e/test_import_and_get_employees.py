import importlib
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.db import Base
from router import app
from router.dependencies import get_employee_service
from scripts import import_employees
from service.employee_service import EmployeeService
import settings

lifespan_module = importlib.import_module("router.lifespan")


class FakeResponse:
    def __init__(self, payload, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


def test_import_then_get_employees_happy_path(monkeypatch, tmp_path) -> None:
    database_path = tmp_path / "employees.db"
    temp_engine = create_engine(
        f"sqlite:///{database_path}", connect_args={"check_same_thread": False}
    )
    temp_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=temp_engine
    )
    Base.metadata.create_all(bind=temp_engine)

    monkeypatch.setattr(settings, "SEED_DB", False)
    monkeypatch.setattr(settings, "FETCH_ON_START", False)
    monkeypatch.setattr(lifespan_module, "engine", temp_engine)

    def fake_post(url, json):
        return FakeResponse(
            {
                "access_token": "token-123",
                "token_type": "bearer",
                "expires_at": (
                    datetime.now(timezone.utc) + timedelta(hours=1)
                ).isoformat(),
            }
        )

    def fake_get(url, headers):
        return FakeResponse(
            [
                {
                    "id": "employee-1",
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "email": "ada@example.com",
                    "date_of_birth": "1815-12-10",
                    "rating": 4.8,
                    "title": "Dr.",
                    "country": "UK",
                    "address": "London",
                    "bio": "Analytical engine pioneer.",
                }
            ]
        )

    monkeypatch.setattr(import_employees.requests, "post", fake_post)
    monkeypatch.setattr(import_employees.requests, "get", fake_get)

    db_session = temp_session_local()

    def fake_get_db():
        return iter([db_session])

    monkeypatch.setattr(import_employees, "get_db", fake_get_db)

    import_employees.run_import()

    app.dependency_overrides[get_employee_service] = lambda: EmployeeService(db_session)

    try:
        with TestClient(app) as client:
            response = client.get("/employees/?offset=0&limit=10&format=json")
    finally:
        app.dependency_overrides.clear()
        db_session.close()

    assert response.status_code == 200

    payload = response.json()

    assert payload["pagination"] == {"total": 1, "offset": 0, "limit": 10}
    assert payload["data"][0]["email"] == "ada@example.com"
    assert payload["data"][0]["first_name"] == "Ada"
