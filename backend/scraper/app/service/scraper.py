import bs4
from playwright.async_api import async_playwright
from loguru import logger

async def playwright_scrape(url: str) -> bs4.BeautifulSoup:
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