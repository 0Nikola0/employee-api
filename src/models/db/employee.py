import uuid

from sqlalchemy import Column, Date, Float, String

from . import Base


class Employee(Base):
    __tablename__ = "employees"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    title = Column(String)
    email = Column(String, unique=True, index=True, nullable=False)
    date_of_birth = Column(Date)
    image = Column(String)
    address = Column(String)
    country = Column(String, index=True)
    bio = Column(String)
    rating = Column(Float, index=True)
