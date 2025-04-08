from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.logging import config_logger
from app.router import scrape

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application dependencies
    """
    config_logger()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(scrape.router, prefix="/scrape", tags=["Scrape"])
