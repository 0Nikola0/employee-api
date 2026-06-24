from pydantic import BaseModel


class PaginationMetadata(BaseModel):
    total: int
    offset: int
    limit: int
