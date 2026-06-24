from sqlalchemy.orm import Session

from models.db import Employee
from repository._generic_repository import GenericRepository


class EmployeeRepository(GenericRepository[Employee]):

    def __init__(self, db: Session):
        super().__init__(db, Employee)
