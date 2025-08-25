from playwright.sync_api import sync_playwright, TimeoutError
from loguru import logger
from app.core.config import settings

def playwright_scrape(url: str, headless: bool = False) -> str:
    """
    Scrape the contents of a page using the Playwright Sync API.
    """
    with sync_playwright() as playwright:
        if headless:
            browser = playwright.chromium.launch(channel="chromium")
        else:
            browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        page = context.new_page()
        try:
            page.goto(url, timeout=settings.PLAYWRIGHT_TIMEOUT)
            content = page.content() 
        except TimeoutError:
            # Ignore timeout errors and continue to the next step
            content = page.content() 
        except Exception as e:
            # throw error for all other exceptions
            raise e
        finally:
            browser.close()
    return content