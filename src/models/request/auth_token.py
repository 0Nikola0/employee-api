from datetime import datetime, timedelta, timezone
from typing import Any

from pydantic import BaseModel, field_validator


class AuthToken(BaseModel):
    access_token: str
    token_type: str
    expires_at: datetime

    @field_validator("expires_at", mode="before")
    @classmethod
    def parse_expires_at(cls, v: Any) -> datetime:

        if isinstance(v, datetime):
            return v

        return datetime.fromisoformat(str(v))

    def is_expired(self, buffer_seconds: int = 30) -> bool:
        return datetime.now(tz=timezone.utc) >= (
            self.expires_at - timedelta(seconds=buffer_seconds)
        )
