import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "Inputs": {
    "input1": [
      {
        "Ratings": 4.47,
        "Price": 94990,
        "Processor": "amd ryzen 9 octa core ",
        "RAM": 16,
        "Operating System": "windows 11",
        "ROM": 1,
        "Display": "13.4",
        "Brand": "ASUS",
        "RAM Type": "LPDDR5",
        "ROM Type": "SSD"
      },
      {
        "Ratings": 4.31,
        "Price": 47990,
        "Processor": "amd ryzen 5 hexa core ",
        "RAM": 8,
        "Operating System": "windows 11",
        "ROM": 512,
        "Display": "15.6",
        "Brand": "MSI",
        "RAM Type": "DDR5",
        "ROM Type": "SSD"
      },
      {
        "Ratings": 4.31,
        "Price": 36990,
        "Processor": "intel core i3  (12th gen)",
        "RAM": 8,
        "Operating System": "windows 11",
        "ROM": 512,
        "Display": "15.6",
        "Brand": "ASUS",
        "RAM Type": "DDR4",
        "ROM Type": "SSD"
      }
    ]
  },
  "GlobalParameters": {}
}

body = str.encode(json.dumps(data))

url = 'http://56906309-5ddb-4c7e-8586-1b32fbcb311d.southindia.azurecontainer.io/score'
# Replace this with the primary/secondary key or AMLToken for the endpoint
api_key = ''
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(error.read().decode("utf8", 'ignore'))
