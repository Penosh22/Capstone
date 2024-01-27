import logging
import json
import azure.functions as func
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from concurrent.futures import ThreadPoolExecutor
import threading

lock = threading.Lock()

def load_page(i):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-images")
    options.add_argument("--disable-css")
    url = f"https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}"
    with lock:
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_3pLy-c row')))
        except TimeoutException:
            print("TimeoutException occurred. The page took too long to load or the element was not found.")
            driver.quit()  # Close the browser
    page_source = driver.page_source
    driver.quit()
    return page_source

def parse_page(page_source):
    mobiles = []
    soup = BeautifulSoup(page_source, 'html.parser')
    divs = soup.find_all('div', class_='_3pLy-c row')

    for div in divs:
        product_name = div.find('div', class_='_4rR01T').text if div.find('div', class_='_4rR01T') else ""
        ratings = div.find('div', class_='gUuXy-').text if div.find('div', class_='gUuXy-') else ""
        price = div.find('div', class_='_30jeq3 _1_WHN1').text if div.find('div', class_='_30jeq3 _1_WHN1') else ""

        features = div.find('ul', class_='_1xgFaf').find_all('li', class_='rgWa7D') if div.find('ul', class_='_1xgFaf') else []
        processor, Ram, ROM, Display, Rear_camera, Front_camera, Battery = "", "", "", "", "", "", ""
        for feature in features:
            feature_text = feature.text
            if "processor" in feature_text.lower():
                processor = feature_text
            elif "RAM" in feature_text:
                Ram = feature_text.split("|")[0] if "|" in feature_text else feature_text
                ROM = feature_text.split("|")[1] if "|" in feature_text else ""
            elif "display" in feature_text.lower():
                Display = feature_text
            elif "camera" in feature_text.lower():
                camera_info = feature_text.split("|")
                Rear_camera = camera_info[0]
                if len(camera_info) > 1:
                    Front_camera = camera_info[1]
            elif "battery" in feature_text.lower():
                Battery = feature_text

        mobile = {
            'Product Name': product_name,
            'Ratings': ratings,
            'Price': price,
            'Processor': processor,
            'RAM': Ram,
            'ROM': ROM,
            'Display': Display,
            'Rear Camera': Rear_camera,
            'Front Camera': Front_camera,
            'Battery': Battery
        }
        mobiles.append(mobile)

    return mobiles

def scrape_and_get_mobiles():
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures_load = [executor.submit(load_page, i) for i in range(1, 60)]
        page_sources = [future.result() for future in futures_load]
        futures_parse = [executor.submit(parse_page, page_source) for page_source in page_sources]
        results = []
        for future in futures_parse:
            results.extend(future.result())
    return results

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    mobiles = scrape_and_get_mobiles()
    return func.HttpResponse(json.dumps(mobiles), status_code=200, mimetype='application/json')
