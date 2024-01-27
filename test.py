from bs4 import BeautifulSoup
from azure.storage.blob import BlobServiceClient
import requests
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException

current_date = datetime.now().strftime("%Y-%m-%d")

# Azure Storage Account information
azure_storage_account_name = input("Enter the azure storage account name: ")
azure_storage_account_key = input("Enter the azure storage account key: ")

# Azure Data Lake Storage container name
container_name = input("Enter the container name: ")

current_date = datetime.now().strftime("%Y-%m-%d")

def get_webpage_content(url: str, max_retries=2, timeout=10) -> str:
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            if response.is_redirect:
                url = response.headers['location']
                print(f"Redirecting to: {url}")
                continue

            print(f"Final URL: {url}")
            return response.text

        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
            if e.response.status_code == 404:
                print("Page not found.")
            return ""
        except requests.exceptions.RequestException as e:
            print(f"RequestException: {e}")
            return ""

def extract_href_from_soup(soup, class_name):
    elements = soup.find_all("a", class_=class_name)
    hrefs = [element.get("href") for element in elements]
    return hrefs

def upload_data_to_azure_storage(data, blob_name):
    blob_service_client = BlobServiceClient(account_url=f"https://{azure_storage_account_name}.blob.core.windows.net", credential=azure_storage_account_key)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data, overwrite=True)

def productDetails(url):
    try:
        content = get_webpage_content(url)
        item_number_title = None
        item_number = None
        soup = BeautifulSoup(content, 'html.parser')
        title_span = soup.find('span', class_='ux-textspans ux-textspans--BOLD')
        title = title_span.text.strip() if title_span else None
        price_div = soup.find('div', class_='x-price-primary')
        
        item_number_div = soup.find('div',class_='ux-layout-section__textual-display ux-layout-section__textual-display--itemId')
        if item_number_div:
            item_number_title_span = item_number_div.find('span',class_='ux-textspans ux-textspans--SECONDARY')
            item_number_title = item_number_title_span.text.strip()
            item_number_span = item_number_div.find('span',class_='ux-textspans ux-textspans--BOLD')
            item_number = item_number_span.text.strip()
        
        price = None
        if price_div:
            price_text_span = price_div.find('span', class_='ux-textspans')
            price = price_text_span.text.strip() if price_text_span else None
        
        main_div = soup.find('div', class_='ux-layout-section-module-evo')
        data_dict = {}
        if main_div:
            rows = main_div.find_all('div', class_='ux-layout-section-evo__row')
            if rows:
                for row_index, row in enumerate(rows, start=1):
                    cols = row.find_all('div', class_='ux-layout-section-evo__col')
                    if cols:
                        for col in cols:
                            labels_div = col.find('div', class_='ux-labels-values__labels-content')
                            values_div = col.find('div', class_='ux-labels-values__values-content')
                            labels_text = labels_div.find('span', class_='ux-textspans').text.strip() if labels_div else None
                            values_text = values_div.find('span', class_='ux-textspans').text.strip() if values_div else None
                            data_dict[labels_text] = values_text
        else:
            print("Main div not found. Check HTML structure.")

        product_det = {
            item_number_title: item_number,
            "Title": title,
            "Price": price,
            "fetchDate": current_date
        }

        product_det.update(data_dict)
        return product_det
    except Exception as e:
        print(f"Error extracting product details from {url}: {e}")
        return {}

def scrape_page(page_number):
    ebay_url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=laptop&_sacat=0&_ipg=240&_pgn={page_number}"
    try:
        content = get_webpage_content(ebay_url)
        soup = BeautifulSoup(content, 'html.parser')
        hrefs = extract_href_from_soup(soup, "s-item__link")

        products = []
        for href in hrefs:
            try:
                product = productDetails(href)
                product['ProductId'] = hrefs.index(href) + 1
                print(product)
                products.append(product)
            except Exception as e:
                print(f"Error extracting details for {href}: {e}")

        return products
    except RequestException as e:
        print(f"Error accessing eBay page {ebay_url}: {e}")
        return []

def scrape_ebay_concurrently(start_page, end_page):
    finalProduct = []

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(scrape_page, range(start_page, end_page + 1)))

    for result in results:
        finalProduct.extend(result)

    data_string = json.dumps(finalProduct, indent=2)
    blob_name = f"ebay_scraped_data_{current_date}.json"
    upload_data_to_azure_storage(data_string, blob_name)

if __name__ == "__main__":
    start_page = 1
    end_page = 40

    try:
        scrape_ebay_concurrently(start_page, end_page)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
