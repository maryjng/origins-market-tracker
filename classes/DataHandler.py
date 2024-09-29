## Parses API request results and compares it to queried data from database. 
## Overwrites, deletes, and adds data to db based on comparisons.

from DatabaseHandler import DatabaseHandler 
from ApiRequestHandler import ApiRequestHandler
from Items import Items 
from models import Shops, Item, User_Item, Shops_Item, User


class DataHandler:
    def __init__(self, db_session, API_URL=None):
        self.api_handler = ApiRequestHandler(API_URL)
        self.db_handler = DatabaseHandler(db_session)

    def get_data_and_timestamp(self):
        request_data = self.api_handler.request_market_data()
        
        # Use `DatabaseHandler` to get the latest timestamp from the database
        latest_timestamp = self.db_handler.get_latest_timestamp()

        return request_data, latest_timestamp
    

        ## ADD ITEM NAME TO THE SHOPS_ITEM TABLE?
    def build_cheapest_shop_list(self, item_ids):
        # Given a list of item_ids, run get_cheapest_shop_by_item() on each id. Build a dictionary for each result and return a list of all these dictionaries.
        cheapest_shops = []

        for item_id in item_ids:
            shop = self.db_handler.get_cheapest_shop_by_item(item_id)

            for owner, title, map_location, map_x, map_y, item_id, item_name, price, timestamp in shop:
                shop = {"name" : item_name,
                        "owner": owner,
                        "title": title,
                        "map_location": map_location,
                        "map_x": map_x,
                        "map_y": map_y,
                        "item_id": item_id,
                        "price": "{:,}".format(price),
                        "timestamp": timestamp}
            
            cheapest_shops.append(shop)

        return cheapest_shops
    
    
    def get_historical_and_current_prices(self, item_id):
        latest_timestamp = self.db_handler.get_latest_timestamp()
        old_shops = []
        current_shops = []

        all_shops = self.db_handler.get_item_shops(item_id)
        for shop in all_shops:
                for owner, title, timestamp, price, map_location, map_x, map_y in shop:
                    shop_data = {"owner": owner,
                                "title": title,
                                "timestamp": timestamp,
                                "price": "{:,}".format(price),
                                "map_location": map_location,
                                "map_x": map_x,
                                "map_y": map_y}
                if shop.req_timestamp == latest_timestamp:
                    current_shops.append(shop_data)
                else:
                    old_shops.append(shop_data)
        
        return old_shops, current_shops
