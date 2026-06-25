import io
import csv

from sqlalchemy import inspect
from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.db import Employee
from models.request import EmployeeCreate
from repository import EmployeeRepository


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.employee_repo = EmployeeRepository(db)

    def get_all_employees(self) -> list[Employee]:
        return self.employee_repo.get_all()

    def get_all_employees_paginated(
        self,
        offset: int = 0,
        limit: int = 10,
        country: str | None = None,
        min_rating: float | None = None,
        sort_by: str | None = None,
    ) -> tuple[list[Employee], int]:
        return self.employee_repo.get_all_paginated(
            offset, limit, country, min_rating, sort_by
        )

    def get_employee_by_id(self, employee_id: int) -> Employee:
        employee = self.employee_repo.get_by_id(employee_id)

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        new_employee = self.employee_repo.create(**employee_data.model_dump())

        return new_employee

    @staticmethod
    def convert_employees_to_csv(employees: list[Employee]) -> str:
        if not employees:
            return ""

        output = io.StringIO()
        writer = csv.writer(output)

        mapper = inspect(employees[0]).mapper
        columns = [column.key for column in mapper.columns]

        writer.writerow(columns)

        for employee in employees:
            writer.writerow([getattr(employee, col) for col in columns])

        return output.getvalue()
