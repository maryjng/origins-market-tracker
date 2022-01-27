import requests

from key import API_KEY
from models import db, connect_db, Item, Shops, Shops_Item, PriceHistory

###############################################################################
# def ping_API():
#     return requests.get("https://api.originsro.org/api/v1/ping")
#
# def whoami():
#     return requests.get("https://api.originsro.org/api/v1/whoami", params={"key": API_KEY})

# def get_all_items():
#     items = requests.get("https://api.originsro.org/api/v1/items/list", params={"api_key": API_KEY})
#     items_res = items.json()
#     items_data = []
#
#     for item in items_res["items"]:
#         dict = {}
#         dict["item_id"] = item["item_id"]
#         dict["unique_name"] = item["unique_name"]
#         dict["name"] = item["name"]
#
#         items_data.append(dict)
#
#     return items_data

#create table for static item data
def populate_items_db():
    items = get_all_items()
    for i in items:
        row = Item(i)
        db.session.add(row)
        db.session.commit()

#automate this request to occur at set intervals
def get_current_data():
    shops = requests.get("https://api.originsro.org/api/v1/market/list", params={"api_key": API_KEY})
    shops_res = shops.json()

    return shops_res

def organize_results(res):
    shops_data = []
    prices_data = []

    #get Shops data
    for shop in res["shops"]:
        shops = {}
        location = shop["location"]

        shops["map_location"] = location["map"]
        shops["map_x"] = location["x"]
        shops["map_y"] = location["y"]
        shops["title"] = shop["title"]
        shops["owner"] = shop["owner"]

        shops_data.append(shops)

        #get PriceHistory data
        for item in res["items"]:
            prices = {}

            prices["item_id"] = item["item_id"]
            prices["cost"] = item["price"]
            prices["owner"] = shop["owner"]
            prices["timestamp"] = res["generation_timestamp"]

            prices_data.append(prices)

    return (shops_data, prices_data)

def store_res_data((shops, prices)):
    all_shops = [Shops(shop) for shop in shops]
    all_prices = [PriceHistory(price) for price in prices]

    try:
        db.session.add(all_shops)
        db.session.add(all_prices)
        db.session.commit()
    except:
        print("Did not work")

def request_and_store_data():
    res = get_current_data()
    (shops_data, prices_data) = organize_results(res)
    store_res_data((shops_data, prices_data))
    print("Done.")

schedule.every(15).minutes.do(request_and_store_data)
