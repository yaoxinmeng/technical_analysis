from playwright.sync_api import sync_playwright
import argparse
import sys
import os

PLAYWRIGHT_TIMEOUT = int(os.environ.get("PLAYWRIGHT_TIMEOUT", "10000"))  # 10 seconds timeout by default

def playwright_scrape(url: str) -> str:
    """
    Scrape the contents of a page using the Playwright Sync API.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        page = context.new_page()
        try:
            page.goto(url, timeout=PLAYWRIGHT_TIMEOUT)
            content = page.content()
        except Exception as e:
            print(f"Error retrieving page content: {e}", file=sys.stderr)
            browser.close()
            sys.exit(1) # Exit if there's an error
        finally:
            browser.close()
    return content

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Playwright Scraper',
        description='Runs playwright in headed mode to scrape a web page.')
    parser.add_argument('url', type=str, help='The URL of the page to scrape.')
    args = parser.parse_args()
    content = playwright_scrape(args.url)
    print(content)