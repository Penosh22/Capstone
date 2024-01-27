
url ='https://www.flipkart.com/search?q=laptop&sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_2_na_na_na&as-pos=1&as-type=RECENT&suggestionId=laptop%7CLaptops&requestId=18952d61-499e-45a8-8958-b4fb54811ead&as-backfill=on&page=1'
import wget
from bs4 import BeautifulSoup
filename = wget.download(url, out='flipkart.html')
# Open the file and parse it with BeautifulSoup
with open('flipkart.html', 'r',encoding="utf8") as f:
    contents = f.read()

soup = BeautifulSoup(contents, 'html.parser')

# Find all divs with class "_3pLy-c row"
divs = soup.find_all('div', class_='_3pLy-c row')

for div in divs:
    try:
        product_name = div.find('div', class_='_4rR01T').text
    except:
        product_name = ""

    try:
        ratings = div.find('div', class_='gUuXy-').text
    except:
        ratings = ""

    try:
        price = div.find('div', class_='_3tbKJL').text
    except:
        price = ""

    try:
        features = div.find('div', class_='fMghEO').find_all('li', class_='rgWa7D')
        processor = features[0].text
        Ram = features[1].text
        Operating_system = features[2].text
        ROM = features[3].text
        Display = features[4].text
    except:
        processor, Ram, Operating_system, ROM, Display = "", "", "", "", ""

    print(f"Product Name: {product_name}")
    print(f"Ratings: {ratings}")
    print(f"Price: {price}")
    print(f"Processor: {processor}")
    print(f"RAM: {Ram}")
    print(f"Operating System: {Operating_system}")
    print(f"ROM: {ROM}")
    print(f"Display: {Display}")
    print("\n")


