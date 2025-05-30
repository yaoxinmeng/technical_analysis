from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from app.core.logging import config_logger
from app.service.yahoo_finance import scrape_price, scrape_main, scrape_financials

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application dependencies
    """
    config_logger()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}


@app.get("/finance/overview/{id}", response_model=dict)
async def get_security_overview(id: str) -> dict:
    """
    Get the overview of a security by its ID.

    :param id: The ID of the security.
    :return: The overview of the security.
    """
    try:
        overview = await scrape_main(id)
        return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/finance/price/{id}", response_model=float)
async def get_security_price(id: str) -> float:
    """
    Get the price of a security by its ID.

    :param id: The ID of the security.
    :return: The price of the security.
    """
    try:
        price = await scrape_price(id)
        return price
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    

@app.get("/finance/financials/{id}", response_model=dict)
async def get_financials(id: str) -> dict:
    """
    Get the financials of a security by its ID.

    :param id: The ID of the security.
    :return: The financials of the security.
    """
    try:
        financials = await scrape_financials(id)
        return financials
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))