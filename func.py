import requests

from sqlalchemy import exc
from key import API_KEY
from models import db, connect_db, Item, Shops, Shops_Item, User
from datetime import timedelta

###############################################################################


def store_results():

    items = [{'item_id': 504, 'name': 'White Potion'}, {'item_id': 505, 'name': 'Blue Potion'}, {'item_id': 506, 'name': 'Green Potion'}, {'item_id': 547, 'name': 'Condensed White Potion'}, {'item_id': 1061, 'name': 'Witch Starsand'}, {'item_id': 12016, 'name': 'Speed Potion'}, {'item_id': 602, 'name': 'Butterfly Wing'}, {'item_id': 605, 'name': 'Anodyne'}, {'item_id': 606, 'name': 'Aloevera'}, {'item_id': 607, 'name': 'Yggdrasil Berry'}, {'item_id': 608, 'name': 'Yggdrasil Seed'}, {'item_id': 645, 'name': 'Concentration Potion'}, {'item_id': 656, 'name': 'Awakening Potion'}, {'item_id': 657, 'name': 'Berserk Potion'}, {'item_id': 662, 'name': 'Authoritative Badge'}, {'item_id': 518, 'name': 'Honey'}, {'item_id': 520, 'name': 'Hinalle Leaflet'}, {'item_id': 521, 'name': 'Aloe Leaflet'}, {'item_id': 522, 'name': 'Mastela Fruit'}, {'item_id': 523, 'name': 'Holy Water'}, {'item_id': 525, 'name': 'Panacea'}, {'item_id': 526, 'name': 'Royal Jelly'}, {'item_id': 678, 'name': 'Poison Bottle'}, {'item_id': 12027, 'name': 'Giggling Box'}, {'item_id': 12028, 'name': 'Box of Thunder'}, {'item_id': 12029, 'name': 'Box of Gloom'}, {'item_id': 12030, 'name': 'Box of Resentment'}, {'item_id': 12031, 'name': 'Box of Drowsiness'}, {'item_id': 12032, 'name': 'Box of Storms'}, {'item_id': 12033, 'name': 'Box of Sunlight'}, {'item_id': 12034, 'name': 'Box of Panting'}, {'item_id': 578, 'name': 'Strawberry'}, {'item_id': 715, 'name': 'Yellow Gemstone'}, {'item_id': 716, 'name': 'Red Gemstone'}, {'item_id': 717, 'name': 'Blue Gemstone'}, {'item_id': 7135, 'name': 'Bottle Grenade'}, {'item_id': 7136, 'name': 'Acid Bottle'}, {'item_id': 7139, 'name': 'Glistening Coat'}, {'item_id': 1025, 'name': 'Cobweb'}, {'item_id': 12041, 'name': 'Fried Grasshopper Legs'}, {'item_id': 12042, 'name': 'Seasoned Sticky Webfoot'}, {'item_id': 12043, 'name': 'Bomber Steak'}, {'item_id': 12044, 'name': 'Herb Marinade Beef'}, {'item_id': 12045, 'name': "Lutie Lady's Pancake"}, {'item_id': 12046, 'name': 'Grape Juice Herbal Tea'}, {'item_id': 12047, 'name': 'Autumn Red Tea'}, {'item_id': 12048, 'name': 'Honey Herbal Tea'}, {'item_id': 12049, 'name': 'Morroc Fruit Wine'}, {'item_id': 12050, 'name': 'Mastela Fruit Wine'}, {'item_id': 12051, 'name': 'Steamed Crab Nippers'}, {'item_id': 12052, 'name': 'Assorted Seafood'}, {'item_id': 12053, 'name': 'Clam Soup'}, {'item_id': 12054, 'name': 'Seasoned Jellyfish'}, {'item_id': 12055, 'name': 'Spicy Fried Bao'}, {'item_id': 12056, 'name': 'Frog Egg and Squid Ink Soup'}, {'item_id': 12057, 'name': 'Smooth Noodle'}, {'item_id': 12058, 'name': 'Tentacle and Cheese Gratin'}, {'item_id': 12059, 'name': 'Lutie Cold Noodle'}, {'item_id': 12060, 'name': 'Steamed Bat Wing in Pumpkin'}, {'item_id': 12061, 'name': 'Honey Grape Juice'}, {'item_id': 12062, 'name': 'Chocolate Mousse Cake'}, {'item_id': 12063, 'name': 'Fruit Mix'}, {'item_id': 12064, 'name': 'Cream Sandwich'}, {'item_id': 12065, 'name': 'Green Salad'}, {'item_id': 12066, 'name': 'Fried Monkey Tails'}, {'item_id': 12067, 'name': 'Mixed Juice'}, {'item_id': 12068, 'name': 'Fried Sweet Potato'}, {'item_id': 12069, 'name': 'Steamed Ancient Lips'}, {'item_id': 12070, 'name': 'Fried Scorpion Tails'}, {'item_id': 12071, 'name': 'Shiny Marinade Beef'}, {'item_id': 12072, 'name': 'Whole Roast'}, {'item_id': 12073, 'name': 'Bearfoot Special'}, {'item_id': 12074, 'name': 'Tendon Satay'}, {'item_id': 12075, 'name': 'Steamed Tongue'}, {'item_id': 12076, 'name': 'Red Mushroom Wine'}, {'item_id': 12077, 'name': 'Special Royal Jelly Herbal Tea'}, {'item_id': 12078, 'name': 'Royal Family Tea'}, {'item_id': 12079, 'name': 'Tristan XII'}, {'item_id': 12080, 'name': 'Dragon Breath Cocktail'}, {'item_id': 12081, 'name': 'Awfully Bitter Bracer'}, {'item_id': 12082, 'name': 'Sumptuous Feast'}, {'item_id': 12083, 'name': 'Giant Burrito'}, {'item_id': 12084, 'name': 'Ascending Dragon Soup'}, {'item_id': 12085, 'name': 'Immortal Stew'}, {'item_id': 12086, 'name': 'Chile Shrimp Gratin'}, {'item_id': 12087, 'name': 'Steamed Alligator with Vegetables'}, {'item_id': 12088, 'name': 'Incredibly Spicy Curry'}, {'item_id': 12089, 'name': 'Special Meat Stew'}, {'item_id': 12090, 'name': 'Steamed Desert Scorpions'}, {'item_id': 12091, 'name': 'Peach Cake'}, {'item_id': 12092, 'name': 'Soul Haunted Bread'}, {'item_id': 12093, 'name': 'Special Toast'}, {'item_id': 12094, 'name': 'Heavenly Fruit Juice'}, {'item_id': 12095, 'name': "Hvergelmir's Tonic"}, {'item_id': 12096, 'name': 'Lucky Soup'}, {'item_id': 12097, 'name': 'Assorted Shish Kebob'}, {'item_id': 12098, 'name': 'Strawberry Flavored Rice Ball'}, {'item_id': 12099, 'name': 'Blood Flavored Soda'}, {'item_id': 12100, 'name': "Cooked Nine Tail's Tails"}, {'item_id': 4133, 'name': 'Raydric Card'}, {'item_id': 4058, 'name': 'Thara Frog Card'}, {'item_id': 4105, 'name': 'Marc Card'}, {'item_id': 4044, 'name': 'Smokie Card'}, {'item_id': 4045, 'name': 'Horn Card'}, {'item_id': 4035, 'name': 'Hydra Card'}, {'item_id': 4252, 'name': 'Alligator Card'}, {'item_id': 4092, 'name': 'Skeleton Worker Card'}, {'item_id': 4082, 'name': 'Desert Wolf Card'}, {'item_id': 4381, 'name': 'Green Ferus Card'}, {'item_id': 4160, 'name': 'Firelock Soldier Card'}, {'item_id': 4170, 'name': 'Dark Frame Card'}, {'item_id': 4107, 'name': 'Verit Card'}, {'item_id': 4064, 'name': 'Zerom Card'}, {'item_id': 4088, 'name': 'Frilldora Card'}, {'item_id': 4097, 'name': 'Matyr Card'}, {'item_id': 4098, 'name': 'Dokebi Card'}, {'item_id': 4099, 'name': 'Pasana Card'}, {'item_id': 4089, 'name': 'Swordfish Card'}, {'item_id': 2115, 'name': "Valkyrja's Shield"}, {'item_id': 2289, 'name': 'Poo Poo Hat'}, {'item_id': 2291, 'name': 'Masquerade'}, {'item_id': 1261, 'name': 'Infiltrator'}, {'item_id': 1264, 'name': 'Specialty Jur'}, {'item_id': 1265, 'name': 'Bloody Roar'}, {'item_id': 2353, 'name': "Odin's Blessing"}, {'item_id': 5128, 'name': "Goibne's Helm"}, {'item_id': 2354, 'name': "Goibne's Armor"}, {'item_id': 2520, 'name': "Goibne's Spaulders"}, {'item_id': 2419, 'name': "Goibne's Greaves"}, {'item_id': 2604, 'name': 'Glove'}, {'item_id': 2624, 'name': 'Glove'}, {'item_id': 2605, 'name': 'Brooch'}, {'item_id': 2625, 'name': 'Brooch [1]'}, {'item_id': 2608, 'name': 'Rosary'}, {'item_id': 2626, 'name': 'Rosary [1]'}, {'item_id': 2607, 'name': 'Clip'}, {'item_id': 2619, 'name': 'Bow Thimble'}, {'item_id': 2671, 'name': 'Bow Thimble [1]'}, {'item_id': 1228, 'name': 'Combat Knife'}, {'item_id': 1525, 'name': 'Long Mace'}, {'item_id': 2502, 'name': 'Hood [1]'}, {'item_id': 2504, 'name': 'Muffler [1]'}, {'item_id': 2506, 'name': 'Manteau [1]'}, {'item_id': 2402, 'name': 'Sandals [1]'}, {'item_id': 2404, 'name': 'Shoes [1]'}, {'item_id': 2406, 'name': 'Boots [1]'}, {'item_id': 2102, 'name': 'Guard [1]'}, {'item_id': 2104, 'name': 'Buckler [1]'}, {'item_id': 2106, 'name': 'Shield [1]'}, {'item_id': 2107, 'name': 'Mirror Shield'}, {'item_id': 2108, 'name': 'Mirror Shield [1]'}, {'item_id': 2121, 'name': 'Memory Book [1]'}, {'item_id': 5170, 'name': 'Feather Beret'}, {'item_id': 2513, 'name': 'Heavenly Maiden Robe'}, {'item_id': 2523, 'name': 'Undershirt [1]'}, {'item_id': 2322, 'name': 'Silk Robe [1]'}, {'item_id': 1705, 'name': 'Composite Bow [4]'}, {'item_id': 1408, 'name': 'Pike [4]'}, {'item_id': 1520, 'name': 'Chain [3]'}, {'item_id': 1208, 'name': 'Main Gauche [4]'}, {'item_id': 1117, 'name': 'Katana [4]'}]

    item_ids = [item["item_id"] for item in items]

    shops = requests.get("https://api.originsro.org/api/v1/market/list", params={"api_key": API_KEY})
    shops_res = shops.json()

    db_shops = Shops.query.all()
    shop_owners = [shop.owner for shop in db_shops]
    # shop_titles = [shop.titles for shop in db_shops]

    #get Shops data
    for shop in shops_res["shops"]:
        for item in shop["items"]:
            if item["item_id"] in item_ids:
                #Check if "owner" and "timestamp" both match for one entry
                if shop["owner"] in shop_owners:
                    owner_shops = Shops.query.filter_by(owner=shops["owner"], timestamp=shop["creation_date"]).first()
                    if len(owner_shops) != 0:
                     #if yes, just update the res_timestamp
                        owner_shops.res_timestamp = shops_res["generation_timestamp"]
                    else:
                     #if no, add entry
                        location = shop["location"]
                        try:
                            db.session.add(Shops(owner=shop["owner"],
                                            timestamp=shop["creation_date"],
                                            title=shop["title"],
                                            map_location=location["map"],
                                            map_x=location["x"],
                                            map_y=location["y"],
                                            req_timestamp = shops_res["generation_timestamp"]
                                        ))
                            
                            shop_id = Shops.query.get(shop_id).filter_by(owner=shop["owner"]).order_by(req_timestamp.desc())
                            
                            db.session.add(Shops_Item(shop_id=shop_id,
                                                    item_id=item["item_id"],
                                                    price=item["price"],
                                                    ))
                        except exc.IntegrityError:
                            db.session.rollback()

    db.session.commit()

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

#
# def get_current_data():
#     shops = requests.get("https://api.originsro.org/api/v1/market/list", params={"api_key": API_KEY})
#     shops_res = shops.json()
#
#     return shops_res
#
#



def request_and_store_data():
    res = get_current_data()
    store_results(res)

    del_threshold = datetime.today() + timedelta(days=-30)
    delete(Shops).where(res_timestamp <= del_threshold)
    #delete rows where timestamp < DATEADD(d, -30, GETDATE())

    print("done running")

#automate the above request and data storage for every 15 mins
# schedule.every(15).minutes.do(request_and_store_data)
