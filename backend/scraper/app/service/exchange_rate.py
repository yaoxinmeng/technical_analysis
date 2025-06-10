from loguru import logger
import requests
import subprocess
import bs4

ROOT_EXCHANGE_URL = "https://www.x-rates.com/calculator"

def get_exchange_rate(curr1: str, curr2: str) -> float | None:
    """
    Get the exchange rate between two currencies.

    :param str curr1: The first currency code.
    :param str curr2: The second currency code.
    :return float: The exchange rate from curr1 to curr2.
    """
    try:
        content = subprocess.check_output(["scripts/playwright_exec.sh", f"{ROOT_EXCHANGE_URL}/?from={curr1}&to={curr2}&amount=1"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        raise Exception(f"{exc.returncode}: {exc.output}")
    soup = bs4.BeautifulSoup(content, "html.parser")
    
    # look for span containing amount
    span_elements = soup.find_all("span")
    span_element = [el for el in span_elements if f"1.00 {curr1}" in el.get_text(strip=True)]
    if not span_element:
        logger.error(f"No span found for {curr1} to {curr2}.")
        return None
    span_element = span_element[0]
    
    # get exchange rate
    data = span_element.find_next_siblings()[0].find_all(text=True, recursive=False)[0]
    logger.debug(data)
    
    return float(data)