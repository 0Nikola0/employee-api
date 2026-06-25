from datetime import date


from pydantic import BaseModel, ConfigDict


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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
    fetched_at: date | None
