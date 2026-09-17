# volunteer connector scraper, scrapes volunteer listings from volunteerconnector.org and returns them in a standardized format

import asyncio
from playwright.async_api import async_playwright

async def scrape_page(request, page_number: int):
    url = f"https://www.volunteerconnector.org/api/search/?page={page_number}" # constructs the URL for the specified page number
    response = await request.get(url); # makes a GET request to the constructed URL

    # print(f"Page {page_number}: HTTP {response.status}"); # Bug Test

    # Error handling for HTTP response status codes --------------------------------------

    if response.status == 404: 
        print(f"Page {page_number} does not exist")
        return page_number, None

    if not response.ok:
        print(f"Failed to fetch page {page_number}: HTTP {response.status}");
        return page_number, []; # returns an empty list if the request fails

    try:
        data = await response.json(); # attempts to parse the response body as JSON
    except Exception as e:
        print(f"Failed to parse JSON for page {page_number}: {e}");
        return page_number, []; # returns an empty list if JSON parsing fails


    return page_number, data; # returns the page number and its parsed JSON data


async def main():
    async with async_playwright() as p: # gives access to playwright

        all_listings = []; # initializes an empty list to hold all volunteer listings
        batch_size = 10; # defines the number of listings to process in each batch
        current_page = 1; # initializes the current page number
        reached_end = False; # flag to indicate if the end of listings has been reached
        
        request = await p.request.new_context(); # creates a new request context for making HTTP requests


        while True: # Scraper loop to continuously scrape pages until there are no more listings

            tasks = [
                scrape_page(request, page_number)
                for page_number in range(current_page, current_page + batch_size)
            ]; # creates a list of tasks for the current batch of pages


            results = await asyncio.gather(*tasks); # runs the tasks concurrently and waits for all of them to complete


            for page_number, data in results:
                if data is None: # If a page does not exist, end the scraper loop
                    reached_end = True;
                    continue;

                all_listings.extend(data); # Add this page's listings to our overall list
                print(f"Page {page_number} finished with {len(data)} listings");

                if len(data) == 0: # If a page has no listings end scraper loop
                    reached_end = True;
            
            if reached_end:
                break;

            current_page += batch_size; # Move to the next batch of pages
        print(f"Total listings: {len(all_listings)}");

        await request.dispose(); # disposes of the request context to free up resources

asyncio.run(main()); # runs the main function in an asynchronous event loop