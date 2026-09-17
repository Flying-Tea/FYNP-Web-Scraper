# entry point for starting scraper and wiring components together (should have very little lines)

import playwright;
from playwright.sync_api import Page, Expect

def test_example(page: Page):
    # Navigate to the example page
    page.goto("https://example.com")

    # Assert that the title is correct
    Expect(page).to_have_title("Example Domain")

    # Click on the More Information link
    page.click("text=More information...")

    # Assert that the new page has the expected URL
    Expect(page).to_have_url("https://www.iana.org/domains/reserved")
