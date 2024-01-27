import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_and_get_laptops():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    for i in range(1, 82):  # Loop through 10 pages
        url = f"https://www.flipkart.com/search?q=laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=laptops%7CLaptops&requestId=896da398-392d-4f33-96e7-ac94efd1b3de&as-searchtext=laptops&page={i}"
        driver.get(url)

        # Parse the downloaded page with BeautifulSoup
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

            print(f"Product Name: {product_name}")
            print(f"Ratings: {ratings}")
            print(f"Price: {price}")
            print(f"Processor: {processor}")
            print(f"RAM: {Ram}")
            print(f"Operating System: {Operating_system}")
            print(f"ROM: {ROM}")
            print(f"Display: {Display}")
            print("\n")

    driver.quit()
scrape_and_get_laptops()