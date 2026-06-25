from typing import cast
from datetime import date

import pytest

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.db import Employee
from service.employee_service import EmployeeService


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


def test_convert_employees_to_csv_returns_header_and_row() -> None:
    csv_output = EmployeeService.convert_employees_to_csv([build_employee()])

    lines = csv_output.strip().splitlines()

    assert lines[0].startswith("id,first_name,last_name,title,email")
    assert "ada@example.com" in lines[1]


def test_get_employee_by_id_raises_404_when_missing() -> None:
    service = EmployeeService(db=cast(Session, object()))
    service.employee_repo = type("Repo", (), {"get_by_id": lambda self, _: None})()

    with pytest.raises(HTTPException) as exc_info:
        service.get_employee_by_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee not found"
