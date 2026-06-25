from contextlib import asynccontextmanager
import logging
import traceback

from fastapi import FastAPI

import settings
from scripts import populate_db, import_employees
from models.db import Base
from repository.conn_setup import engine

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):

    Base.metadata.create_all(bind=engine)

    if settings.FETCH_ON_START:
        try:
            import_employees.run_import()
        except Exception as e:
            logger.error(
                f"Importing employees failed with error {e}. \nTraceback: {traceback.format_exc()}"
            )

    if settings.SEED_DB:
        try:
            populate_db.populate()
        except Exception as e:
            logger.error(
                f"Seeding database failed with error {e}. \nTraceback: {traceback.format_exc()}"
            )

    yield
