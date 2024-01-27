# original azure working code

import logging
import json
import azure.functions as func
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor

def scrape_page(i):
    laptops = []
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    url = f"https://www.flipkart.com/search?q=laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=laptops%7CLaptops&requestId=896da398-392d-4f33-96e7-ac94efd1b3de&as-searchtext=laptops&page={i}"
    try:
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
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

            laptop = {
                'Product Name': product_name,
                'Ratings': ratings,
                'Price': price,
                'Processor': processor,
                'RAM': Ram,
                'Operating System': Operating_system,
                'ROM': ROM,
                'Display': Display
            }
            laptops.append(laptop)

    except Exception as e:
        logging.error(f"Error loading page {i}: {e}")
    finally:
        driver.quit()

    return laptops

def scrape_and_get_laptops():
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(scrape_page, i) for i in range(1, 82)]
        results = []
        for future in futures:
            results.extend(future.result())
    return results

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    laptops = scrape_and_get_laptops()
    return func.HttpResponse(json.dumps(laptops), status_code=200, mimetype='application/json')
