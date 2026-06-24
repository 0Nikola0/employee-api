from datetime import date

from pydantic import BaseModel


class EmployeeResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    title: str | None
    email: str
    date_of_birth: date | None
    image: str | None
    address: str | None
    country: str | None
    bio: str | None
    rating: float | None

    class Config:
        from_attributes = True
