import requests
import schedule

import json
from sqlalchemy import exc
from sqlalchemy.sql import func
from key import API_KEY
from models import db, connect_db, Item, Shops, Shops_Item, User

###############################################################################

def store_results():
    items_raw = db.session.query(Item.id).all()
    items_ids = [item[0].id for item in items_raw]

    res = requests.get("https://api.originsro.org/api/v1/market/list", params={"api_key": API_KEY})
    shops_res = res.json()

    # f = open('newshops.json')
    # shops_res = json.load(f)

    db_shops = Shops.query.all()
    shop_owners = [shop.owner for shop in db_shops]
    #gets list of shop owners in database

    shops = [shop for shop in shops_res if shop["type"]=="V"]
    for shop in shops:
        #filter out the items we don't care about
        shop_items = [item for item in shop if item["item_id"] in item_ids]
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
                                req_timestamp = shops_res["generation_timestamp"]
                                ))

                    db.session.flush()

                    latest = db.session.query(func.max(Shops.id)).first()[0]
    #                 latest_shop = latest[0]

                for item in shop_items:
                    stock = Shops_Item(shop_id=latest.id, item_id=item["item_id"], price=item["price"])
                    latest.stock.append(stock)
            else:
                saved_shop.req_timestamp = shops_res["generation_timestamp"]
                    
    db.session.commit()


def get_current_data():
    shops = requests.get("https://api.originsro.org/api/v1/market/list", params={"api_key": API_KEY})
    shops_res = shops.json()
    out_file = open("newshops.json", "w")
    json.dump(shops_res, out_file, indent = 6)
    out_file.close()

    # return shops_res


def request_and_store_data():
    store_results()

    del_threshold = datetime.today() - timedelta(days=30)
    delete(Shops).where(res_timestamp <= del_threshold)
    db.session.commit()
    #delete rows where timestamp < DATEADD(d, -30, GETDATE())

    print("done running")

#automate the above request and data storage for every 15 mins
def automate():
    schedule.every(15).minutes.do(request_and_store_data)
