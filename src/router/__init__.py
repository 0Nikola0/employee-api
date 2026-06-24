from fastapi import FastAPI

from router.routes import employee_routes
from router.lifespan import lifespan

app = FastAPI(
    title="Employees API",
    version="1.0.0",
    openapi_tags=[
        {"name": "Employees"},
    ],
    lifespan=lifespan
)

app.include_router(employee_routes.router)
