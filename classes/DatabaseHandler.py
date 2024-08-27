class DatabaseHandler:
    def __init__(self, db_session):
        self.db_session = db_session

    # def store_data(self, data):
    #     # Store the data in the database
    #     for item in data:
    #         shop = Shops(
    #             owner=item['owner'],
    #             title=item['title'],
    #             map_location=item['map_location'],
    #             map_x=item['map_x'],
    #             map_y=item['map_y'],
    #             item_id=item['item_id'],
    #             price=item['price'],
    #             timestamp=item['timestamp']
    #         )
    #         self.db_session.add(shop)
    #     self.db_session.commit()


    def upsert_shop(self, shop_data, generation_timestamp):
        # Check if the shop already exists based on owner and timestamp
        existing_shop = self.db_session.query(Shops).filter_by(
            owner=shop_data['owner'], 
            timestamp=shop_data['timestamp']
        ).first()

        if existing_shop:
            # Update existing shop req_timestamp and get the ShopID
            existing_shop.req_timestamp = generation_timestamp

            #query all shops_item using ShopID
            #for queried_item in existing_shop:
                #compare to counterpart in shop_data["items"]
                    #if no match, delete the row
                    #if match, update the row

        else:
            # Create a new shop record
            new_shop = Shops(
                owner=shop_data['owner'],
                title=shop_data['title'],
                map_location=shop_data['map_location'],
                map_x=shop_data['map_x'],
                map_y=shop_data['map_y'],
                item_id=shop_data['item_id'],
                price=shop_data['price'],
                timestamp=shop_data['timestamp']
            )
            self.db_session.add(new_shop)

        self.db_session.commit()




    def update_latest_timestamp(self, timestamp):
        # Update the metadata table with the latest timestamp
        self.db_session.execute(
            "UPDATE ApiRequestMetadata SET latest_request_timestamp = :timestamp WHERE id = 1",
            {"timestamp": timestamp}
        )
        self.db_session.commit()

    def get_latest_timestamp(self):
        # Get the latest timestamp from the metadata table
        return self.db_session.query(ApiRequestMetadata.latest_request_timestamp).filter_by(id=1).scalar()

# CREATE TABLE ApiRequestMetadata (
#     id INT PRIMARY KEY,
#     latest_request_timestamp TIMESTAMP
# );