from models import Shops

class ReqResultHandler:
    def __init__(self, db_session, db_handler, api_handler):
        self.db_session = db_session
        self.db_handler = db_handler
        self.api_handler = api_handler

    def filter_shops(self):
        results = self.api_handler.request_shop_data()

        items_ids = #get all item IDs

        shops_res = [shop for shop in results["shops"] if shop["type"]=="V"]
        #get the selling shops from the response

        generation_timestamp = results["generation_timestamp"]
        #get the generation timestamp from results for Shop req_timestamp col

        # Upsert the shop data
        for shop_data in shops_res:
            self.db_handler.upsert_shop(shop_data, generation_timestamp)