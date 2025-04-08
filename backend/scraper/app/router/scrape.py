import traceback

from fastapi import APIRouter, HTTPException
from loguru import logger

from app.schema.financial_data import FinancialData
from app.service.agent import extract_information

router = APIRouter()

@router.get(path="/{name}", response_model=FinancialData)
def search_venues(name: str) -> FinancialData:
    try:
        return extract_information(name)
    except BaseException as e:
        logger.error(traceback.format_exc())
        raise HTTPException(400, repr(e))