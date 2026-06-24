from contextlib import asynccontextmanager

from fastapi import FastAPI

from models.db import Base
from repository.conn_setup import engine


@asynccontextmanager
async def lifespan(_: FastAPI):

    Base.metadata.create_all(bind=engine)

    yield
