from typing import TypeVar, Generic

from sqlalchemy.orm import Session


T = TypeVar("T")


class GenericRepository(Generic[T]):

    def __init__(self, db: Session, model_class):
        self.db = db
        self.model_class = model_class

    def get_all(self) -> list[T]:
        return self.db.query(self.model_class).all()

    def get_by_id(self, id: int) -> T | None:
        return self.db.query(self.model_class).filter(self.model_class.id == id).first()

    def create(self, **kwargs) -> T:
        obj = self.model_class(**kwargs)
        self.db.add(obj)
        self.db.commit()
        return obj

    def update(self, id: int, **kwargs) -> T | None:
        obj = self.get_by_id(id)
        if not obj:
            raise ValueError(f"{self.model_class.__name__} with id {id} not found")

        for key, value in kwargs.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
        self.db.commit()

        return obj

    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if not obj:
            raise ValueError(f"{self.model_class.__name__} with id {id} not found")

        self.db.delete(obj)
        self.db.commit()
        return True

    def exists(self, id: int) -> bool:
        return (
            self.db.query(self.model_class).filter(self.model_class.id == id).first()
            is not None
        )

    def get_all_paginated(self, offset: int, limit: int) -> tuple[list[T], int]:
        offset = max(0, offset)
        limit = min(max(1, limit), 100)

        query = (
            self.db.query(self.model_class)
            .order_by(self.model_class.id)
        )

        total_count = query.count()
        records = query.offset(offset).limit(limit).all()

        return records, total_count
