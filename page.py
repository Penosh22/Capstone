
# Your list of URLs
urls = [f'https://www.flipkart.com/search?q=laptops&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&otracker1=AS_QueryStore_OrganicAutoSuggest_1_7_na_na_ps&as-pos=1&as-type=RECENT&suggestionId=laptops%7CLaptops&requestId=896da398-392d-4f33-96e7-ac94efd1b3de&as-searchtext=laptops&page={i}' for i in range(10)]
import wget

for i, url in enumerate(urls):
    try:
        # Download the URL and save it as an HTML file
        filename = wget.download(url, out=f'page{i}.html')
        print(f'\nDownloaded {url} as {filename}')

    except Exception as e:
        print(f"Error occurred for URL {url}: {str(e)}")
