## Parses API request results and compares it to queried data from database. 
## Overwrites, deletes, and adds data to db based on comparisons.

from DatabaseHandler import DatabaseHandler 
from ApiRequestHandler import ApiRequestHandler
from Items import Items 
from models import Shops, Item, User_Item, Shops_Item, User


class ReqResultHandler:
    def __init__(self, db_session):
        self.db_session = db_session
        self.request_data = ApiRequestHandler.request_shop_data()
        self.latest_timestamp = DatabaseHandler.get_latest_timestamp()


    def store_shop_data(self, request_data):
        for item in request_data:
            shop = Shops(
                owner=item['owner'],
                title=item['title'],
                map_location=item['map_location'],
                map_x=item['map_x'],
                map_y=item['map_y'],
                item_id=item['item_id'],
                price=item['price'],
                timestamp=item['timestamp']
            )

    def filter_shops(self):
        # res = ApiRequestHandler.request_shop_data()
        # latest_timestamp = ApiRequestHandler.get_latest_timestamp(res)

        # query Shops using owner and creation timestamp
            # for each item in the queried shop:
                # if the item doesn't exist in res shop, add to historical sales
                # if the item exists but the amount is less than in the db, add to historical sales
        # if there is no owner/creation timestamp match, save the Shop and all Shops_Item
        pass
