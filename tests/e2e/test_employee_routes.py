from datetime import date

from fastapi.testclient import TestClient

from models.db import Employee
from router import app
from router.dependencies import get_employee_service


def build_employee() -> Employee:
    return Employee(
        id="employee-1",
        first_name="Ada",
        last_name="Lovelace",
        title="Dr.",
        email="ada@example.com",
        date_of_birth=date(1815, 12, 10),
        image=None,
        address="London",
        country="UK",
        bio="Analytical engine pioneer.",
        rating=4.8,
        fetched_at=date(2026, 6, 25),
    )


class FakeEmployeeService:
    def __init__(self) -> None:
        self.employee = build_employee()

    def get_all_employees_paginated(
        self,
        offset: int = 0,
        limit: int = 10,
        country: str | None = None,
        min_rating: float | None = None,
        sort_by: str | None = None,
    ) -> tuple[list[Employee], int]:
        return [self.employee], 1


def test_get_employees_happy_path_returns_paginated_json() -> None:
    app.dependency_overrides[get_employee_service] = lambda: FakeEmployeeService()

    try:
        client = TestClient(app)
        response = client.get("/employees/?offset=0&limit=10&format=json")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    payload = response.json()

    assert payload["pagination"] == {"total": 1, "offset": 0, "limit": 10}
    assert payload["data"][0]["email"] == "ada@example.com"
    assert payload["data"][0]["first_name"] == "Ada"
