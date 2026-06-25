from pydantic import BaseModel
from typing import Generic, TypeVar

from .pagination_metadata import PaginationMetadata

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: list[T]
    pagination: PaginationMetadata
