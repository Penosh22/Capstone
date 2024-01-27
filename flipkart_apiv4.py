from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

app = FastAPI()

class Laptop(BaseModel):
    product_name: str
    ratings: Optional[str]
    price: str
    processor: Optional[str]
    RAM: Optional[str]
    Operating_system: Optional[str]
    ROM: Optional[str]
    Display: Optional[str]

@app.get("/scrape/laptops", response_model=List[Laptop])
async def scrape_and_get_laptops():
    laptops = []  # This will store your laptops data
    browser = await launch()
    tasks = []
    for i in range(1, 100):  # Loop through 10 pages
        tasks.append(scrape_page(i, browser, laptops))
    await asyncio.gather(*tasks)
    await browser.close()
    return laptops

async def scrape_page(i, browser, laptops):
    page = await browser.newPage()
    url = f"https://www.flipkart.com/search?q=laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=laptops%7CLaptops&requestId=896da398-392d-4f33-96e7-ac94efd1b3de&as-searchtext=laptops&page={i}"

    # Disable timeout
    await page.goto(url, timeout=0)

    # Optimize page load by blocking unnecessary resources
    await page.setRequestInterception(True)
    page.on('request', lambda req: asyncio.ensure_future(intercept_request(req)))
    content = await page.content()

    # Parse the downloaded page with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.select('div._3pLy-c.row')

    for div in divs:
        product_name = div.select_one('div._4rR01T').text if div.select_one('div._4rR01T') else ""
        ratings = div.select_one('div.gUuXy-').text if div.select_one('div.gUuXy-') else ""
        price = div.select_one('div._3tbKJL').text if div.select_one('div._3tbKJL') else ""

        features = div.select('div.fMghEO li.rgWa7D') if div.select_one('div.fMghEO') else []
        processor, Ram, Operating_system, ROM, Display = "", "", "", "", ""
        for feature in features:
            if "processor" in feature.text.lower():
                processor = feature.text
            elif "RAM" in feature.text:
                Ram = feature.text
            elif "display" in feature.text.lower():
                Display = feature.text
            elif "system" in feature.text.lower():
                Operating_system = feature.text
            elif "SSD" in feature.text or "HDD" in feature.text:
                ROM = feature.text

        laptop = Laptop(
            product_name=product_name,
            ratings=ratings,
            price=price,
            processor=processor,
            RAM=Ram,
            Operating_system=Operating_system,
            ROM=ROM,
            Display=Display
        )
        laptops.append(laptop.dict())
    await page.close()

# Define a function to intercept and abort requests for images, CSS, or fonts
async def intercept_request(req):
    if req.resourceType in ['image', 'stylesheet', 'font']:
        await req.abort()
    else:
        await req.continue_()
