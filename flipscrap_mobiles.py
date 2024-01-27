from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

def wait_for_page_load(driver, timeout=30):
    WebDriverWait(driver, timeout).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

def scrape_and_get_mobiles():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    for i in range(1, 401):  # Loop through 400 pages
        url = f"https://www.flipkart.com/search?q=mobile&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={i}"
        driver.get(url)
        wait_for_page_load(driver)  # Wait until the page has finished loading

        # Parse the downloaded page with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        divs = soup.find_all('div', class_='_3pLy-c row')

        for div in divs:
            product_name = div.find('div', class_='_4rR01T').text if div.find('div', class_='_4rR01T') else ""
            ratings = div.find('div', class_='gUuXy-').text if div.find('div', class_='gUuXy-') else ""
            price = div.find('div', class_='_3tbKJL').text if div.find('div', class_='_3tbKJL') else ""

            features = div.find('div', class_='fMghEO').find_all('li', class_='rgWa7D') if div.find('div', class_='fMghEO') else []
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

            print(f"Product Name: {product_name}")
            print(f"Ratings: {ratings}")
            print(f"Price: {price}")
            print(f"Processor: {processor}")
            print(f"RAM: {Ram}")
            print(f"ROM: {ROM}")
            print(f"Display: {Display}")
            print(f"Rear Camera: {Rear_camera}")
            print(f"Front Camera: {Front_camera}")
            print(f"Battery: {Battery}")
            print("\n")

    driver.quit()

scrape_and_get_mobiles()
