import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    url = "https://www.flipkart.com/search?q=laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=laptops%7CLaptops&requestId=896da398-392d-4f33-96e7-ac94efd1b3de&as-searchtext=laptops&page=1"
    await page.goto(url)
    content = await page.content()
    with open('flipkart.html', 'w', encoding='utf-8') as f:
        f.write(content)
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
