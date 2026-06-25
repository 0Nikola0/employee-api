import logging
from datetime import datetime, date
from typing import Any

from pydantic import BaseModel, EmailStr, field_validator, model_validator

logger = logging.getLogger(__name__)


class EmployeeCreate(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    date_of_birth: date
    title: str | None = None
    address: str | None = None
    country: str | None = None
    bio: str | None = None
    rating: float
    image: str | None = None
    fetched_at: datetime | None = None

    @field_validator("rating", mode="before")
    @classmethod
    def coerce_rating(cls, v: Any) -> float:
        return float(v)

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def parse_date(cls, v: Any) -> date:
        if isinstance(v, date):
            return v
        return date.fromisoformat(str(v))

    @model_validator(mode="before")
    @classmethod
    def warn_unknown_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            known = {
                "id",
                "first_name",
                "last_name",
                "email",
                "date_of_birth",
                "title",
                "address",
                "country",
                "bio",
                "rating",
                "image",
                "fetched_at",
            }

            for key in data:
                if key not in known:
                    logger.warning(
                        "Unknown field in employee payload: %r — ignoring", key
                    )

        return data
