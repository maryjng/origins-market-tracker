import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from key import USERNAME, PASSWORD

from models import db, User, Item, Shops, Shops_Item, User_Item

os.environ['DATABASE_URL'] = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/markettest?client_encoding=utf8"

from app import app

db.create_all()

###
#SETUP
###
class ShopsModelTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        shop1 = Shops(owner="test_owner",
                    title="test_shoptitle",
                    map_location="prontera",
                    map_x="123",
                    map_y="321",
                    timestamp="2022-02-05T22:01:46Z",
                    req_timestamp="2022-02-06T16:44:01.91Z")

        shop1id = 1
        shop1.id = shop1id

        db.session.add(shop1)

        shop1 = Shops.query.get(shop1id)
        self.shop1 = shop1
        self.shop1_id = shop1id


        #now add items
        item1 = Item(id="504", name="White Potion")
        item1id = 504
        item1.id = item1id

        item2 = Item(id="505", name="Blue Potion")
        item2id = 505
        item2.id = item2id

        db.session.add(item1, item2)

        db.session.commit()

        item1 = Item.query.get(504)
        self.item1 = item1
        self.item1.id = item1id

        item2 = Item.query.get(505)
        self.item2 = item2
        self.item2.id = item2id


        #now add shops_items
        stock1 = Shops_Item(shop_id="1", item_id=item1.id, price="1337")
        stock2 = Shops_Item(shop_id="1", item_id=item2.id, price="42069")

        db.session.add(stock1, stock2)

        stock = db.session.query(Shops_Item).filter_by(shop_id=="1").all()
        stock1 = stock[0]
        self.stock1 = stock1

        stock2 = stock[1]
        self.stock2 = stock2

        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()
###

#tests the db.relationship between Shops and Shops_Item (Shops.stock)
    def test_curr_items_relationship(self):
        self.assertEqual(shop1.stock, [stock1, stock2])

###
#Test class method
###

    def test_search_method_works(self):
        shop = Shops.check_if_in_db("test_owner", "2022-02-05T22:01:46Z")
        self.assertEqual(shop.id, 1)

    def test_search_method_none(self):
        shop = Shops.check_if_in_db("shopthatdoesntexist", "1999-05-01")
        self.assertEqual(shop.id, None)
