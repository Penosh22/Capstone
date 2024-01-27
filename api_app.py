from flask import Flask, jsonify
from bs4 import BeautifulSoup
import wget

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape():
    # Your list of URLs
    urls = [f'https://www.amazon.in/s?i=computers&rh=n%3A1375424031&fs=true&page=2&qid=1699510603&ref=sr_pg_{i}' for i in range(10)]

    data = []

    for i, url in enumerate(urls):
        try:
            # Download the URL and save it as an HTML file
            filename = wget.download(url, out=f'page{i}.html')

            # Open the file and parse it with BeautifulSoup
            with open(f'page{i}.html', 'r') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Find all divs with the specified class
            divs = soup.find_all('div', class_='a-section a-spacing-small puis-padding-left-small puis-padding-right-small')

            # Iterate over each div and extract the required information
            for div in divs:
                product = {}
                try:
                    product['description'] = div.find('span', class_='a-size-base-plus a-color-base a-text-normal').text
                except:
                    product['description'] = ""
                try:
                    product['price'] = div.find('span', class_='a-price-whole').text
                except:
                    product['price'] = ""
                try:
                    product['rating'] = div.find('span', class_='a-icon-alt').text
                except:
                    product['rating'] = ""
                try:
                    product['remark'] = div.find('span', class_='a-badge-text', attrs={'data-a-badge-color': 'sx-cloud'}).text
                except:
                    product['remark'] = ""
                try:
                    product['discount'] = div.find('span', class_='a-letter-space').text
                except:
                    product['discount'] = ""
                
                # Append the extracted data to the data list
                data.append(product)

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

