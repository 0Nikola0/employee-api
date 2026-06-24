import time
import logging
import functools
from typing import Callable, Any
from datetime import datetime, timezone

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

import settings
from repository.conn_setup import get_db
from models.request import EmployeeCreate, AuthToken
from service.employee_service import EmployeeService

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def get_token() -> str:
    logger.info("Authenticating...")

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
        
    return token.access_token


def get_employees(token: str) -> list[EmployeeCreate]:
    logger.info("Fetching employees")

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


if __name__ == "__main__":
    token = get_token()
    employees = get_employees(token)

    if not employees:
        logger.warning("No employees")

    else:
        emp_service = EmployeeService(get_db())

        for e in employees:
            emp_service.create_employee(e)

        logger.info(f"Stored {len(employees)} employees")
