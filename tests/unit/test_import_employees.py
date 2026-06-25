from datetime import date, datetime, timedelta, timezone
from types import SimpleNamespace

import requests

from scripts import import_employees


class FakeResponse:
    def __init__(self, payload, status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(response=self)


def test_token_manager_fetches_and_caches_token(monkeypatch) -> None:
    calls = []

    def fake_post(url, json):
        calls.append((url, json))
        return FakeResponse(
            {
                "access_token": "token-123",
                "token_type": "bearer",
                "expires_at": (
                    datetime.now(timezone.utc) + timedelta(hours=1)
                ).isoformat(),
            }
        )

    monkeypatch.setattr(import_employees.requests, "post", fake_post)

    manager = import_employees.TokenCacheManager()

    first_token = manager.get_token()
    second_token = manager.get_token()

    assert first_token == "token-123"
    assert second_token == "token-123"
    assert len(calls) == 1
    assert calls[0][0].endswith("/api/token/")


def test_get_employees_uses_token_and_parses_records(monkeypatch) -> None:
    requested = {}

    def fake_get(url, headers):
        requested["url"] = url
        requested["headers"] = headers
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
                }
            ]
        )

    monkeypatch.setattr(import_employees.requests, "get", fake_get)

    employees = import_employees.get_employees(
        SimpleNamespace(get_token=lambda: "token-123")
    )

    assert requested["url"].endswith("/api/employee/list/")
    assert requested["headers"] == {"Access-Token": "token-123"}
    assert len(employees) == 1
    assert employees[0].email == "ada@example.com"
    assert employees[0].date_of_birth == date(1815, 12, 10)
