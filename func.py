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
    items = [item[0] for item in items_raw]

    shops = requests.get("https://api.originsro.org/api/v1/market/list", params={"api_key": API_KEY})
    shops_res = shops.json()

    # f = open('newshops.json')
    # shops_res = json.load(f)

    db_shops = Shops.query.all()
    shop_owners = [shop.owner for shop in db_shops]
    #gets list of shop owners in database

    for shop in shops_res["shops"]:
        if shop["type"] == "V":
            for item in shop["items"]:
                if item["item_id"] in items:
                    owner_shops = db.session.query(Shops).filter(Shops.owner==shop["owner"]).filter(Shops.timestamp==shop["creation_date"]).first()
                    if shop["owner"] in shop_owners and owner_shops:
                        #just update the res_timestamp
                        owner_shops.res_timestamp = shops_res["generation_timestamp"]

                    else:
                     #if no, add entry
                        location = shop["location"]
                        # try:
                        new_shop = db.session.add(Shops(owner=shop["owner"],
                                        title=shop["title"],
                                        map_location=location["map"],
                                        map_x=location["x"],
                                        map_y=location["y"],
                                        timestamp=shop["creation_date"],
                                        req_timestamp = shops_res["generation_timestamp"]
                                    ))

                        latest = db.session.query(func.max(Shops.id)).first()
                        latest_shop = latest[0]

                        db.session.add(Shops_Item(shop_id=latest_shop,
                                                item_id=item["item_id"],
                                                price=item["price"],
                                                ))
                        # # except exc.IntegrityError:
                        #     db.session.rollback()
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
