class DatabaseHandler:
    def __init__(self, db_session):
        self.db_session = db_session

    def store_data(self, data):
        # Store the data in the database
        for item in data:
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
            self.db_session.add(shop)
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