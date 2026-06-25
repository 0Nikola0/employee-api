from typing import Literal, Union

from fastapi import APIRouter, Depends, Query, Response

from models.response import EmployeeResponse
from router.dependencies import get_employee_service
from service.employee_service import EmployeeService
from models.response.paginated_response import PaginatedResponse, PaginationMetadata

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=Union[PaginatedResponse[EmployeeResponse], str])
def get_all_employees(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    country: str | None = Query(None, description="Exact country match"),
    min_rating: float | None = Query(None, ge=0, description="Minimum employee rating"),
    sort_by: (
        Literal["first_name", "last_name", "rating", "date_of_birth"] | None
    ) = Query(
        None,
        description="Field to sort by",
    ),
    format: Literal["json", "csv"] = Query(
        "json", description="Format of returned data"
    ),
    employee_service: EmployeeService = Depends(get_employee_service),
):
    employees, total = employee_service.get_all_employees_paginated(
        offset=offset,
        limit=limit,
        country=country,
        min_rating=min_rating,
        sort_by=sort_by,
    )

    if format == "csv":
        csv_content = employee_service.convert_employees_to_csv(employees)

        return Response(
            content=csv_content,
            media_type="text/csv",
            headers={
                "x-total-count": str(total),
                "x-offset": str(offset),
                "x-limit": str(limit),
            },
        )

    pagination = PaginationMetadata(
        total=total,
        offset=offset,
        limit=limit,
    )

    return PaginatedResponse[EmployeeResponse](data=employees, pagination=pagination)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee_by_id(
    employee_id: int,
    employee_service: EmployeeService = Depends(get_employee_service),
):

    return employee_service.get_employee_by_id(employee_id)
