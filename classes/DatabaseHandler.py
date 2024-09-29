from models import db, Shops, Item, User_Item, Shops_Item, User, Metadata

class DatabaseHandler:
    def __init__(self, db_session): #this is sqlalchemy's db.session. Pass it in app.py
        self.db_session = db_session

    def update_latest_timestamp(self, timestamp):
        # Update the metadata table with the latest timestamp
        self.db_session.execute(
            "UPDATE Metadata SET latest_request_timestamp = :timestamp WHERE id = 1",
            {"timestamp": timestamp}
        )
        self.db_session.commit()

    def get_latest_timestamp(self):
        # Get the latest timestamp from the metadata table
        res = self.db_session.query(Metadata).first()
        return res.latest_request_timestamp if res else None
    
    def get_cheapest_shop_by_item(self, item_id):
        # Return shop that has cheapest stock of item_id. Includes shop details, item_id, and price. 
        # Only includes shops that are open according to most recent API request (looking at shop req_timestamp)
        latest_timestamp = self.get_latest_timestamp()
        shop = (db.session.query(Shops.owner,
                    Shops.title,
                    Shops.map_location,
                    Shops.map_x,
                    Shops.map_y,
                    Shops_Item.item_id,
                    Shops_Item.price,
                    Shops.timestamp)
            .join(Shops_Item)
            .filter(Shops_Item.item_id==item_id, Shops.req_timestamp==latest_timestamp)
            .order_by(Shops_Item.price.asc())
            .limit(1)
            .all())

        return shop
        
    def get_item_shops(self, item_id):
        # This returns all the shops that currently are selling and have sold the item. 
        historical = (db.session.query(Shops.owner,
                                    Shops.title,
                                    Shops.timestamp,
                                    Shops_Item.price,
                                    Shops.map_location,
                                    Shops.map_x,
                                    Shops.map_y)
                                    .join(Shops_Item)
                                    .filter(Shops_Item.item_id==item_id)
                                    .order_by(Shops_Item.price.asc())
                                    .all())
        
        return historical

# CREATE TABLE ApiRequestMetadata (
#     id INT PRIMARY KEY,
#     latest_request_timestamp TIMESTAMP
# );