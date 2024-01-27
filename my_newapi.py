import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin

async def get_webpage_content(url: str, max_retries=3, timeout=10) -> str:
    async with httpx.AsyncClient() as client:
        for attempt in range(max_retries):
            try:
                response = await client.get(url, timeout=timeout)
                response.raise_for_status()
                return response.text
            except (httpx.RequestError, httpx.TimeoutException) as exc:
                print(f"Attempt {attempt + 1} failed. Retrying...")
                await asyncio.sleep(2 ** attempt)
        else:
            raise exc

async def scrape_href_links(content: str, target_class: str) -> list:
    soup = BeautifulSoup(content, 'html.parser')
    base_url = "https://www.amazon.in"  # Set the base URL if needed

    href_links = [urljoin(base_url, a['href']) for a in soup.find_all('a', {'class': target_class}, href=True)]
    return href_links

async def scrape_product_details(url: str) -> dict:
    content = await get_webpage_content(url)
    soup = BeautifulSoup(content, 'html.parser')

    product_details = {}

    # Scraping from the first table (id="productDetails_techSpec_section_1")
    table_1 = soup.find('table', {'id': 'productDetails_techSpec_section_1'})
    if table_1:
        rows = table_1.find_all('tr')
        for row in rows:
            key = row.find('th', {'class': 'a-color-secondary a-size-base prodDetSectionEntry'})
            value = row.find('td', {'class': 'a-size-base prodDetAttrValue'})
            if key and value:
                product_details[key.text.strip()] = value.text.strip().replace('\u200e', '')

    # Scraping from the second table (id="productDetails_detailBullets_sections1", class="a-keyvalue prodDetTable")
    table_2 = soup.find('table', {'id': 'productDetails_detailBullets_sections1', 'class': 'a-keyvalue prodDetTable'})
    if table_2:
        rows = table_2.find_all('tr')
        for row in rows:
            key = row.find('th', {'class': 'a-color-secondary a-size-base prodDetSectionEntry'})
            value = row.find('td', {'class': 'a-size-base prodDetAttrValue'})
            if key and value:
                product_details[key.text.strip()] = value.text.strip()

    # Remove fields with empty values
    product_details = {k: v for k, v in product_details.items() if v}
    
    # Scraping from span with id="productTitle"
    product_title_span = soup.find('span', {'id': 'productTitle'})
    product_title = product_title_span.text.strip() if product_title_span else "No product title found"

    # Add product title to the existing dictionary
    product_details['Title'] = product_title

    # Scraping from span with class="a-size-base a-color-base"
    additional_span = soup.find('span', {'class': 'a-size-base a-color-base'})
    additional_text = additional_span.text.strip() if additional_span else "No additional text found"

    # Add the additional text to the existing dictionary
    product_details['Rating (out of 5)'] = additional_text

    return product_details

async def main():
    for i in range(1, 20):
        await asyncio.sleep(20)
        amazon_url = f"https://www.amazon.in/s?k=laptop&page={i}&crid=2PR9G4NVATT3&qid=1699686221&sprefix=laptop%2Caps%2C272"
        content = await get_webpage_content(amazon_url)
        target_class = "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"
        href_links = await scrape_href_links(content, target_class)
        for link in href_links:
            amazon_product_url = link
            details = await scrape_product_details(amazon_product_url)
            print("\nScraped Product Details:")
            print(details)

            # Create a separate file for each product
            output_filename = f"output_{i}.txt"
            with open(output_filename, 'w', encoding='utf-8') as file:
                file.write(str(details))

if __name__ == "__main__":
    asyncio.run(main())
