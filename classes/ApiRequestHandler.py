import os
import requests
from models import Shops, Item, User_Item, Shops_Item, User

class ApiRequestHandler:
    def __init__(self, URL):
        self.API_KEY = os.environ.get('API_KEY')
        self.URL = URL
        ##take out the URL and either add it as part of init params or .env var

    def request_market_data(self):
        # Make the API request and return the data
        shops = requests.get(self.URL, params={"api_key": self.API_KEY})
        res = shops.json()
        return res
