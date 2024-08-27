## Parses API request results and compares it to queried data from database. 
## Overwrites, deletes, and adds data to db based on comparisons.

import DatabaseHandler from DatabaseHandler
import ApiRequestHandler from ApiRequestHandler
import Items from Items

class ReqResultHandler:
    def __init__(self, db_session):
        self.db_session = db_session

    def filter_shops(self):
        # res = ApiRequestHandler.request_shop_data()
        # latest_timestamp = ApiRequestHandler.get_latest_timestamp(res)

        # query Shops using owner and creation timestamp
            # for each item in the queried shop:
                # if the item doesn't exist in res shop, add to historical sales
                # if the item exists but the amount is less than in the db, add to historical sales
        # if there is no owner/creation timestamp match, save the Shop and all Shops_Item

