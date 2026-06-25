from sqlalchemy.orm import Session

from models.db import Employee
from repository._generic_repository import GenericRepository


class EmployeeRepository(GenericRepository[Employee]):

    def __init__(self, db: Session):
        super().__init__(db, Employee)

    def get_all_paginated(
        self,
        offset: int = 0,
        limit: int = 10,
        country: str | None = None,
        min_rating: float | None = None,
        sort_by: str | None = None,
    ) -> tuple[list[Employee], int]:
        offset = max(0, offset)
        limit = min(max(1, limit), 100)

        query = self.db.query(self.model_class)

        if country is not None:
            query = query.filter(self.model_class.country == country)

        if min_rating is not None:
            query = query.filter(self.model_class.rating >= min_rating)

        if sort_by is not None:
            query = query.order_by(
                getattr(self.model_class, sort_by), self.model_class.id
            )
        else:
            query = query.order_by(self.model_class.id)

        total_count = query.count()
        records = query.offset(offset).limit(limit).all()

        return records, total_count
