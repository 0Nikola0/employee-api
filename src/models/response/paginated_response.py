from pydantic import BaseModel
from .pagination_metadata import PaginationMetadata


class PaginatedResponse(BaseModel):
    data: list
    pagination: PaginationMetadata
