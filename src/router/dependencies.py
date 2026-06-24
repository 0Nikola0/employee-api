from fastapi import Depends
from sqlalchemy.orm import Session

from repository.conn_setup import get_db
from service.employee_service import EmployeeService


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)