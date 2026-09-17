# volunteer connector scraper, scrapes volunteer listings from volunteerconnector.org and returns them in a standardized format

import asyncio
from playwright.async_api import async_playwright

async def scrape_page(request, page_number: int):
    url = f"https://www.volunteerconnector.org/api/search/?page={page_number}" # constructs the URL for the specified page number
    response = await request.get(url) # makes a GET request to the constructed URL
    data = await response.json() # parses the response body as JSON
    return data # returns the parsed JSON data


async def main():
    async with async_playwright() as p: # gives access to playwright

        request = await p.request.new_context(); # creates a new request context for making HTTP requests

        tasks = [scrape_page(request, page_number) for page_number in range(1, 6)] # creates a list of tasks to scrape pages 1 to 5

        results = await asyncio.gather(*tasks) # runs the tasks concurrently and waits for all of them to complete

        for page_number, data in enumerate(results, start=1):
            # Goes through each result while keeping track of its page number

            print(f"\n--- PAGE {page_number} ---")
            # Prints a separator so we can distinguish the pages

            print(data)
            # Prints the data returned from that page


        await request.dispose() # disposes of the request context to free up resources

asyncio.run(main()) # runs the main function in an asynchronous event loop