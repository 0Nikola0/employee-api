import time
import logging
import functools
from typing import Callable, Any
from datetime import datetime, timezone

if __name__ == "__main__":
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from models.db import Base
import settings as settings
from repository.conn_setup import get_db, engine
from models.request import EmployeeCreate, AuthToken
from service.employee_service import EmployeeService

logger = logging.getLogger(__name__)


class TokenCacheManager:
    def __init__(self):
        self.token: AuthToken | None = None

    def get_token(self) -> str:
        if self.token and not self.token.is_expired():
            return self.token.access_token

        response = requests.post(
            f"{settings.BASE_URL}/api/token/",
            json={
                "grant_type": "password",
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
                "username": settings.USERNAME,
                "password": settings.PASSWORD,
            },
        )

        response.raise_for_status()

        token = AuthToken.model_validate(response.json())

        if token.is_expired():
            logger.error("Token is already expired")
            raise ValueError("Token is alredy expired")

        self.token = token
        return self.token.access_token


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: int = 1,
    backoff_factor: int = 2,
    max_delay: int = 60,
):

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)

                except RequestException as e:
                    last_exception = e

                    if isinstance(e, (Timeout, ConnectionError)):
                        transient = True
                    elif hasattr(e, "response") and e.response:
                        transient = (
                            e.response.status_code >= 500
                            or e.response.status_code == 429
                        )
                    else:
                        transient = False

                    if transient and attempt < max_retries - 1:
                        time.sleep(delay)
                        delay = min(delay * backoff_factor, max_delay)
                        continue

                    raise

            raise last_exception or RuntimeError("Max retries exhausted")

        return wrapper

    return decorator


@retry_with_backoff()
def get_employees(token_manager: TokenCacheManager) -> list[EmployeeCreate]:
    token = token_manager.get_token()

    response = requests.get(
        f"{settings.BASE_URL}/api/employee/list/",
        headers={"Access-Token": token},
    )

    response.raise_for_status()

    fetched_at = datetime.now(tz=timezone.utc)
    employees = []

    for record in response.json():
        try:
            record["fetched_at"] = fetched_at
            employees.append(EmployeeCreate.model_validate(record))

        except Exception:
            logger.warning(f"Skipping invalid record {record.get('id')}")

    logger.info(f"Fetched {len(employees)} employees")

    return employees


def run_import() -> None:
    print("Importing employees")

    token_manager = TokenCacheManager()
    employees = get_employees(token_manager)

    if not employees:
        logger.warning("No employees")

    else:
        db_session = next(get_db())
        emp_service = EmployeeService(db_session)

        for e in employees:
            emp_service.create_employee(e)

        logger.info(f"Stored {len(employees)} employees")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    run_import()
