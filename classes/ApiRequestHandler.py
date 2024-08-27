import os

class ApiRequestHandler:
    def __init__(self):
        self.API_KEY = os.environ.get('API_KEY')
        self.URL = "https://api.originsro.org/api/v1/market/list"
        ##take out the URL and either add it as part of init params or .env var

    def request_shop_data():
        # Make the API request and return the data
        shops = requests.get(URL, params={"api_key": API_KEY})
        res = shops.json()
        return res
