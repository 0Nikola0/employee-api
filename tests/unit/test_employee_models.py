from datetime import date, datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from models.request import AuthToken, EmployeeCreate


def test_employee_create_coerces_date_and_rating() -> None:
    employee = EmployeeCreate.model_validate(
        {
            "id": "employee-1",
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@example.com",
            "date_of_birth": "1815-12-10",
            "rating": "4.8",
            "fetched_at": "2026-06-25T12:00:00+00:00",
        }
    )

    assert employee.date_of_birth == date(1815, 12, 10)
    assert employee.rating == 4.8
    assert employee.email == "ada@example.com"


def test_employee_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        EmployeeCreate.model_validate(
            {
                "id": "employee-1",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "email": "not-an-email",
                "date_of_birth": "1815-12-10",
                "rating": 4.8,
            }
        )


def test_auth_token_parses_expiry_and_reports_not_expired() -> None:
    token = AuthToken.model_validate(
        {
            "access_token": "token-123",
            "token_type": "bearer",
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(minutes=5)
            ).isoformat(),
        }
    )

    assert token.access_token == "token-123"
    assert token.is_expired() is False
