import json
import azure.functions as func
import logging
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional   
import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup

class Laptop(BaseModel):
    product_name: str
    ratings: Optional[str]
    price: str
    processor: Optional[str]
    RAM: Optional[str]
    Operating_system: Optional[str]
    ROM: Optional[str]
    Display: Optional[str]

laptops = []
async def scrape_and_get_laptops():
    browser = await launch()
    page = await browser.newPage()
    for i in range(1, 82):  # Loop through 10 pages
        url = f"https://www.flipkart.com/search?q=laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=laptops%7CLaptops&requestId=896da398-392d-4f33-96e7-ac94efd1b3de&as-searchtext=laptops&page={i}"
        await page.goto(url,timeout=0)
        content = await page.content()

        # Parse the downloaded page with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        divs = soup.find_all('div', class_='_3pLy-c row')

        for div in divs:
            product_name = div.find('div', class_='_4rR01T').text if div.find('div', class_='_4rR01T') else ""
            ratings = div.find('div', class_='gUuXy-').text if div.find('div', class_='gUuXy-') else ""
            price = div.find('div', class_='_3tbKJL').text if div.find('div', class_='_3tbKJL') else ""

            features = div.find('div', class_='fMghEO').find_all('li', class_='rgWa7D') if div.find('div', class_='fMghEO') else []
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

    await browser.close()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse(json.dumps(laptops),mimetype='text/json',status_code=200)    