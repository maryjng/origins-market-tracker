import requests
import json

from datetime import datetime, timedelta
from sqlalchemy import exc, delete
from sqlalchemy.sql import func

from key import API_KEY
from models import db, connect_db, Item, Shops, Shops_Item, User

###############################################################################

def store_results():
    items_raw = db.session.query(Item.id).all()
    item_ids = [item[0] for item in items_raw]

    shops = requests.get("https://api.originsro.org/api/v1/market/list", params={"api_key": API_KEY})
    res = shops.json()
    shops_res = res["shops"]

    db_shops = Shops.query.all()
    shop_owners = [shop.owner for shop in db_shops]
    #gets list of shop owners in database

    shops = [shop for shop in shops_res if shop['type']=="V"]
    for shop in shops:
        #filter out the items we don't care about
        shop_items = [item for item in shop["items"] if item["item_id"] in item_ids]
        shop_item_ids = [item["item_id"] for item in shop_items]

        if len(shop_item_ids) > 0:
            saved_shop = Shops.check_if_in_db(shop["owner"], shop["creation_date"])

            if saved_shop == None:
                location = shop["location"]

                db.session.add(Shops(owner=shop["owner"],
                            title=shop["title"],
                            map_location=location["map"],
                            map_x=location["x"],
                            map_y=location["y"],
                            timestamp=shop["creation_date"],
                            req_timestamp = res["generation_timestamp"]
                            ))

                db.session.flush()

                latest = db.session.query(func.max(Shops.id)).first()[0]
                latest_shop = Shops.query.get(latest)

                for item in shop_items:
                    saved_stock = db.session.query(Shops_Item).filter_by(item_id=item["item_id"], shop_id=latest).one_or_none()
                    if saved_stock == None:
                        stock = Shops_Item(shop_id=latest, item_id=item["item_id"], price=item["price"])
                        latest_shop.stock.append(stock)

                        db.session.flush()

            else:
                saved_shop.req_timestamp = res["generation_timestamp"]

    db.session.commit()

    
def request_and_store_data():
    store_results()

    del_threshold = datetime.today() - timedelta(days=15)
    delete(Shops).where(Shops.req_timestamp <= del_threshold)
    db.session.commit()

    print("done running" + datetime.today())

