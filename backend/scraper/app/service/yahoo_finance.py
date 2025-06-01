import re
import subprocess
from loguru import logger
import bs4

ROOT_YAHOO_URL = "https://sg.finance.yahoo.com/quote"


def scrape_main(id: str) -> dict[str, str]:
    """
    Scrape the main page.
    """
    content = subprocess.check_output(["scripts/playwright_exec.sh", f"{ROOT_YAHOO_URL}/{id}"], stderr=subprocess.STDOUT)
    soup = bs4.BeautifulSoup(content, "html.parser")
    results = {"sector": "", "exchange_currency": "", "name": ""}

    # scrape name
    h1_elements = soup.find_all("h1")
    name_elements = [el for el in h1_elements if id in el.get_text(strip=True)]
    if not name_elements:
        logger.error(f"No name found for {id}.")
    else:
        if len(name_elements) > 1:
            logger.warning(f"Multiple name elements found for {id}. Using the first one.")
            logger.debug(f"Found elements: {name_elements}")
        name = name_elements[0].get_text(strip=True)
        name = re.sub(r"\s*\(.*?\)\s*", "", name)  # remove any text in parentheses
        results["name"] = name

    # scrape sector information
    elements = soup.find_all(string="Sector")
    if not elements:
        logger.error(f"No sector information found for {id}.")
    else:
        if len(elements) > 1:
            logger.warning(f"Multiple sector elements found for {id}. Using the first one.")
            logger.debug(f"Found elements: {elements}")
        parent = elements[0].find_parent()
        siblings = parent.find_previous_siblings() + parent.find_next_siblings()
        results["sector"] = siblings[0].get_text(strip=True)
    
    # scrape currency information
    currency_element_parent = soup.find("span", attrs={"class": "exchange"})
    if not currency_element_parent:
        logger.error(f"No currency information found for {id}.")
    else:
        currency_element = currency_element_parent.find_all("span")[-1]
        if not currency_element:
            logger.error(f"No currency information found for {id}.")
            return {}
        results["exchange_currency"] = currency_element.get_text(strip=True)
    
    return results


def scrape_price(id: str) -> float:
    """
    Scrape the price page.
    """
    content = subprocess.check_output(["scripts/playwright_exec.sh", f"{ROOT_YAHOO_URL}/{id}/history"], stderr=subprocess.STDOUT)
    soup = bs4.BeautifulSoup(content, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        logger.error(f"No table found in page for {id}.")
        return -1
    if len(tables) > 1:
        logger.warning(f"Multiple tables found for {id}. Using the first one.")
        logger.debug(f"Found tables: {tables}")
    table = tables[0]

    # get header row
    header_row = table.find("thead").find("tr")
    if not header_row:
        logger.error(f"No header row found in table for {id}.")
        return -1
    headers = [th.get_text(strip=True) for th in header_row.find_all("th")]

    # get index of close price
    close_index = None
    for i, h in enumerate(headers):
        if "close" in h.lower():
            close_index = i
            break
    if close_index is None:
        logger.error(f"Close price not found in headers for {id}.")
        return -1

    # get first row of data
    first_row = table.find("tbody").find("tr")
    if not first_row:
        logger.error(f"No data rows found in table for {id}.")
        return -1
    data = [td.get_text(strip=True) for td in first_row.find_all("td")]

    # convert close price to float
    try:
        price = float(data[close_index].replace(",", ""))
    except ValueError as e:
        logger.error(f"Error converting close price to float for {id}: {e}")
        return 0
    
    return price


def scrape_financial_statement(id: str) -> dict[str, dict[str, int]]:
    """
    Scrape the financial statement page.
    """
    content = subprocess.check_output(["scripts/playwright_exec.sh", f"{ROOT_YAHOO_URL}/{id}/financials"], stderr=subprocess.STDOUT)
    soup = bs4.BeautifulSoup(content, "html.parser")

    def parse_financials_table(soup: bs4.BeautifulSoup) -> dict[str, int]:
        """
        Parse a financials table and return a dictionary of financial data.
        """
        header_div = soup.find("div", attrs={"class": "tableHeader"})
        headers = [div.get_text(strip=True) for div in header_div.find("div").find_all("div")]
        if len(headers) < 2:
            logger.error(f"Not enough headers found in financials page for {id}.")
            logger.debug(f"Headers found: {headers}")
            return {}
        headers = headers[1:] 

        # get relevant data rows
        income_row = soup.find("div", string="Diluted NI available to com stockholders").find_parent().find_next_siblings()
        if len(income_row) < 2:
            logger.error(f"Not enough data rows found in financials page for {id}.")
            return {}
        shares_row = soup.find("div", string="Diluted average shares").find_parent().find_next_siblings()
        if len(shares_row) < 2:
            logger.error(f"Not enough data rows found in financials page for {id}.")
            return {}
        
        results = {}
        for h, income, shares in zip(headers, income_row, shares_row):
            income_value = income.get_text(strip=True).replace(",", "")
            shares_value = shares.get_text(strip=True).replace(",", "")
            try:
                results[h] = {
                    "income": int(float(income_value) * 1000) if income_value else None,
                    "shares": int(float(shares_value) * 1000) if shares_value else None
                }
            except ValueError as e:
                logger.error(f"Error converting financial data to float for {h} in {id}: {e}")
                continue 
        return results   

    def parse_currency(soup: bs4.BeautifulSoup) -> str:
        """
        Parse the currency from the financials page.
        """
        currency_span = soup.find("span", string=re.compile("Currency in .*"))
        if not currency_span:
            logger.error(f"No currency information found in financials page for {id}.")
            return ""
        currency_text = currency_span.get_text(strip=True)
        currency_match = re.search(r"Currency in (.+)", currency_text)
        currency = currency_match.group(1)
        return currency.strip()
    
    return {"financials_currency": parse_currency(soup), "financials": parse_financials_table(soup)}


def scrape_balance(id: str) -> dict[str, dict[str, int]]:
    """
    Scrape the balance sheet page.
    """
    content = subprocess.check_output(["scripts/playwright_exec.sh", f"{ROOT_YAHOO_URL}/{id}/balance-sheet"], stderr=subprocess.STDOUT)
    soup = bs4.BeautifulSoup(content, "html.parser")
    
    header_div = soup.find("div", attrs={"class": "tableHeader"})
    headers = [div.get_text(strip=True) for div in header_div.find("div").find_all("div")]
    if len(headers) < 2:
        logger.error(f"Not enough headers found in balance sheet page for {id}.")
        logger.debug(f"Headers found: {headers}")
        return {}
    headers = headers[1:]  # skip the first header which is usually the date

    # get relevant data rows
    assets_row = soup.find("div", string="Total assets").find_parent().find_next_siblings()
    if len(assets_row) < 2:
        logger.error(f"Not enough data rows found in balance sheet page for {id}.")
        return {}
    liabilities_row = soup.find("div", string="Total liabilities net minority interest").find_parent().find_next_siblings()
    if len(liabilities_row) < 2:
        logger.error(f"Not enough data rows found in balance sheet page for {id}.")
        return {}
    book_value_row = soup.find("div", string="Tangible book value").find_parent().find_next_siblings()
    if len(book_value_row) < 2:
        logger.error(f"Not enough data rows found in balance sheet page for {id}.")
        return {}
    
    results = {}
    for h, assets, liabilities, book_value in zip(headers, assets_row, liabilities_row, book_value_row):
        assets_value = assets.get_text(strip=True).replace(",", "")
        liabilities_value = liabilities.get_text(strip=True).replace(",", "")
        book_value_value = book_value.get_text(strip=True).replace(",", "")
        try:
            results[h] = {
                "assets": int(float(assets_value) * 1000) if assets_value else None,
                "liabilities": int(float(liabilities_value) * 1000) if liabilities_value else None,
                "book_value": int(float(book_value_value) * 1000) if book_value_value else None
            }
        except ValueError as e:
            logger.error(f"Error converting balance sheet data to float for {h} in {id}: {e}")
            continue
    
    return results