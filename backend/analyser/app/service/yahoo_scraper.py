import re
from loguru import logger
import bs4
from playwright.async_api import async_playwright

ROOT_YAHOO_URL = "https://sg.finance.yahoo.com/quote"

async def scrape(id: str) -> str:
    """
    Call to scrape the contents of a web page. Retrieves only textual elements and images.

    :param str url: The URL of the web page to scrape.
    :return str: The content of the web page rendered in Markdown.
    """
    # scrape sector information
    results = await asyncio.gather(
        scrape_main(id),
        scrape_financials(id),
        scrape_balance(id),
        scrape_price(id)
    )

    return {"overview": results[0], "financials": results[1], "balance-sheet": results[2], "price": results[3]}


async def scrape_main(id: str) -> dict[str, str]:
    """
    Scrape the main page.
    """
    soup = await _playwright_scrape(f"{ROOT_YAHOO_URL}/{id}")

    # scrape sector information
    elements = soup.find_all(string="Sector")
    if not elements:
        logger.error(f"No sector information found for {id}.")
        return ""
    if len(elements) > 1:
        logger.warning(f"Multiple sector elements found for {id}. Using the first one.")
        logger.debug(f"Found elements: {elements}")
    
    parent = elements[0].find_parent()
    siblings = parent.find_previous_siblings() + parent.find_next_siblings()
    sector = siblings[0].get_text(strip=True)

    if not siblings:
        logger.error(f"No siblings found for sector element of {id}.")
        return ""
    if len(siblings) > 1:
        logger.warning(f"Multiple siblings found for sector element of {id}. Using the first one.")
        logger.debug(f"Found siblings: {siblings}")
    
    # scrape currency information
    currency_element_parent = soup.find("span", attrs={"class": "exchange"})
    if not currency_element_parent:
        logger.error(f"No currency information found for {id}.")
        return ""
    currency_element = currency_element_parent.find_all("span")[-1]
    if not currency_element:
        logger.error(f"No currency information found for {id}.")
        return ""
    currency = currency_element.get_text(strip=True)
    
    return {"sector": sector, "exchange_currency": currency}


async def scrape_price(id: str) -> str:
    """
    Scrape the price page.
    """
    soup = await _playwright_scrape(f"{ROOT_YAHOO_URL}/{id}/history")
    tables = soup.find_all("table")
    if not tables:
        logger.error(f"No table found in page for {id}.")
        return ""
    if len(tables) > 1:
        logger.warning(f"Multiple tables found for {id}. Using the first one.")
        logger.debug(f"Found tables: {tables}")
    table = tables[0]

    # get header row
    header_row = table.find("thead").find("tr")
    if not header_row:
        logger.error(f"No header row found in table for {id}.")
        return ""
    headers = [th.get_text(strip=True) for th in header_row.find_all("th")]

    # get index of close price
    close_index = None
    for i, h in enumerate(headers):
        if "close" in h.lower():
            close_index = i
            break
    if close_index is None:
        logger.error(f"Close price not found in headers for {id}.")
        return ""

    # get first row of data
    first_row = table.find("tbody").find("tr")
    if not first_row:
        logger.error(f"No data rows found in table for {id}.")
        return ""
    data = [td.get_text(strip=True) for td in first_row.find_all("td")]

    return data[close_index]


async def scrape_financials(id: str) -> dict[str, dict[str, int]]:
    """
    Scrape the financials page.
    """
    soup = await _playwright_scrape(f"{ROOT_YAHOO_URL}/{id}/financials")
    header_div = soup.find("div", attrs={"class": "tableHeader"})
    headers = [div.get_text(strip=True) for div in header_div.find("div").find_all("div")]
    if len(headers) < 2:
        logger.error(f"Not enough headers found in financials page for {id}.")
        logger.debug(f"Headers found: {headers}")
        return ""
    headers = headers[1:] 

    # get relevant data rows
    income_row = soup.find("div", string="Diluted NI available to com stockholders").find_parent().find_next_siblings()
    if len(income_row) < 2:
        logger.error(f"Not enough data rows found in financials page for {id}.")
        return ""
    shares_row = soup.find("div", string="Diluted average shares").find_parent().find_next_siblings()
    if len(shares_row) < 2:
        logger.error(f"Not enough data rows found in financials page for {id}.")
        return ""
    
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

    # get currency info
    currency_span = soup.find("span", string=re.compile("Currency in .*"))
    if not currency_span:
        logger.error(f"No currency information found in financials page for {id}.")
        return ""
    currency_text = currency_span.get_text(strip=True)
    currency_match = re.search(r"Currency in (.+)", currency_text)
    currency = currency_match.group(1)
    results["financials_currency"] = currency.strip()
    
    return results


async def scrape_balance(id: str) -> dict[str, dict[str, int]]:
    """
    Scrape the balance sheet page.
    """
    soup = await _playwright_scrape(f"{ROOT_YAHOO_URL}/{id}/balance-sheet")
    header_div = soup.find("div", attrs={"class": "tableHeader"})
    headers = [div.get_text(strip=True) for div in header_div.find("div").find_all("div")]
    if len(headers) < 2:
        logger.error(f"Not enough headers found in balance sheet page for {id}.")
        logger.debug(f"Headers found: {headers}")
        return ""
    headers = headers[1:]  # skip the first header which is usually the date

    # get relevant data rows
    assets_row = soup.find("div", string="Total assets").find_parent().find_next_siblings()
    if len(assets_row) < 2:
        logger.error(f"Not enough data rows found in balance sheet page for {id}.")
        return ""
    liabilities_row = soup.find("div", string="Total liabilities net minority interest").find_parent().find_next_siblings()
    if len(liabilities_row) < 2:
        logger.error(f"Not enough data rows found in balance sheet page for {id}.")
        return ""
    book_value_row = soup.find("div", string="Tangible book value").find_parent().find_next_siblings()
    if len(book_value_row) < 2:
        logger.error(f"Not enough data rows found in balance sheet page for {id}.")
        return ""
    
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


async def _playwright_scrape(url: str) -> bs4.BeautifulSoup:
    """
    Scrape the contents of a page using the Playwright Sync API.
    """
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        page = await context.new_page()
        try:
            await page.goto(url, timeout=10000)  # 10 seconds timeout
        except Exception as e:
            logger.error(f"Error loading page: {e}") 
        try:    # attempts to retrieve page contents regardless
            content = await page.content()
        except Exception as e:
            logger.error(f"Error retrieving page content: {e}") 
            content = ""
        await browser.close()
    return bs4.BeautifulSoup(content, "html.parser")


if __name__ == "__main__":
    import asyncio
    # Example usage
    content = asyncio.run(scrape_main("0005.HK"))
    print("Overview:")
    print(content)
    content = asyncio.run(scrape_price("0005.HK"))
    print("Price Information:")
    print(content)
    content = asyncio.run(scrape_financials("0005.HK"))
    print("Financials Information:")
    print(content)
    content = asyncio.run(scrape_balance("0005.HK"))
    print("Balance Sheet Information:")
    print(content)