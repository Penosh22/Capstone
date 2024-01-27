from bs4 import BeautifulSoup

# Open the file and parse it with BeautifulSoup
for i in range(10):
    with open(f'page{i}.html', 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

# Find all divs with the specified class
divs = soup.find_all('div', class_='a-section a-spacing-small puis-padding-left-small puis-padding-right-small')

# Initialize empty lists to store the extracted data
product_descriptions = []
prices = []
ratings = []
product_remarks = []
discounts = []

# Iterate over each div and extract the required information
for div in divs:
    try:
        product_description = div.find('span', class_='a-size-base-plus a-color-base a-text-normal').text
    except:
        product_description = ""
    try:
        price = div.find('span', class_='a-price-whole').text
    except:
        price = ""
    try:
        rating = div.find('span', class_='a-icon-alt').text
    except:
        rating = ""
    try:
        product_remark = div.find('span', class_='a-badge-text', attrs={'data-a-badge-color': 'sx-cloud'}).text
    except:
        product_remark = ""
    try:
        discount = div.find('span', class_='a-letter-space').text
    except:
        discount = ""
    
    # Append the extracted data to the respective lists
    product_descriptions.append(product_description)
    prices.append(price)
    ratings.append(rating)
    product_remarks.append(product_remark)
    discounts.append(discount)

# Print all the values in the given columns
for pd, p, r, pr, d in zip(product_descriptions, prices, ratings, product_remarks, discounts):
    print(f'Product Description: {pd}, Price: {p}, Rating: {r}, Product Remark: {pr}, Discount: {d}')



