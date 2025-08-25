from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from loguru import logger
import traceback

from app.core.logging import config_logger
from app.service.yahoo_finance import scrape_price, scrape_main, scrape_financial_statement, scrape_balance
from app.service.exchange_rate import get_exchange_rate

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application dependencies
    """
    config_logger()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the service is running.
    """
    return {"status": "ok"}


@app.get("/finance/overview/{id}", response_model=dict)
def get_security_overview(id: str) -> dict:
    """
    Get the overview of a security by its ID.

    :param id: The ID of the security.
    :return: The overview of the security.
    """
    try:
        overview = scrape_main(id)
        return overview
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/finance/price/{id}", response_model=float)
def get_security_price(id: str) -> float:
    """
    Get the price of a security by its ID.

    :param id: The ID of the security.
    :return: The price of the security.
    """
    try:
        price = scrape_price(id)
        return price
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/finance/financials/{id}", response_model=dict)
def get_financials(id: str) -> dict:
    """
    Get the financials of a security by its ID.

    :param id: The ID of the security.
    :return: The financials of the security.
    """
    try:
        financials = {
            "financial_statement": scrape_financial_statement(id), 
            "balance_sheet": scrape_balance(id)
        }
        return financials
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/exchange/{curr1}/{curr2}", response_model=float)
def get_exchange(curr1: str, curr2: str) -> float:
    """
    Get the exchange rate between two currencies.

    :param curr1: The first currency code.
    :param curr2: The second currency code.
    :return: The exchange rate from curr1 to curr2.
    """
    try:
        rate = get_exchange_rate(curr1, curr2)
        if rate is None:
            raise HTTPException(status_code=404, detail="Exchange rate not found")
        return rate
    except Exception as e:
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, lifespan="on")