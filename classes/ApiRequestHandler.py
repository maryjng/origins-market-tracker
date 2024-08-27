import os

class ApiRequestHandler:
    def __init__(self):
        self.API_KEY = os.environ.get('API_KEY')
        self.MARKET_URL = "https://api.originsro.org/api/v1/market/list"

    def request_shop_data():
        # Make the API request and return the data
        shops = requests.get(MARKET_URL, params={"api_key": API_KEY})
        res = shops.json()
        return res

    def get_latest_timestamp(self, data):
        # Extract the latest timestamp from the data
        return max(item['timestamp'] for item in data)