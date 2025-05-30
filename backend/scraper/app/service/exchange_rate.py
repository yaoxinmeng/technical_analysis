from loguru import logger
import requests

from app.service.scraper import playwright_scrape

ROOT_EXCHANGE_URL = "https://www.xe.com/api"

def get_exchange_rate(curr1: str, curr2: str) -> float:
    """
    Get the exchange rate between two currencies.

    :param str curr1: The first currency code.
    :param str curr2: The second currency code.
    :return float: The exchange rate from curr1 to curr2.
    """
    url = f"{ROOT_EXCHANGE_URL}/protected/statistics/?from={curr1}&to={curr2}"
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        logger.error(f"Failed to fetch exchange rate from {curr1} to {curr2}. Status code: {response.status_code}")
        return None
    data = response.json()
    if "last1Days" not in data or "average" not in data["last1Days"]:
        logger.error(f"Invalid response format for exchange rate from {curr1} to {curr2}.")
        return None
    
    return data["last1Days"]["average"]