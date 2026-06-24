from fastapi import APIRouter, Depends, Query

from models.response import EmployeeResponse
from models.response.paginated_response import PaginatedResponse, PaginationMetadata
from router.dependencies import get_employee_service
from service.employee_service import EmployeeService

router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=PaginatedResponse)
def get_all_employees(
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page"),
    employee_service: EmployeeService = Depends(get_employee_service),
):
    employees, total = employee_service.get_all_employees_paginated(offset, limit)

    pagination = PaginationMetadata(
        total=total,
        offset=offset,
        limit=limit,
    )

    return PaginatedResponse(data=employees, pagination=pagination)

@router.get("/{employee_id:int}", response_model=list[EmployeeResponse])
def get_employee_by_id(
    employee_id: int,
    employee_service: EmployeeService = Depends(get_employee_service),
):

    return employee_service.get_employee_by_id(employee_id)
