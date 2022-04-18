import os
from unittest import TestCase
from flask_bcrypt import Bcrypt
from sqlalchemy import exc
from key import USERNAME, PASSWORD

from models import db, User, Item, Shops_Item, User_Item

os.environ['DATABASE_URL'] = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/markettest"


from app import app

db.create_all()

class ItemModelsTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()


    def test_item_model(self):
        """Does the basic model work?"""

        i = Item(id=504, name="White Potion")

        db.session.add(i)
        db.session.commit()

        items = Item.query.all()

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "White Potion")


    ###
    # Test class method
    ###
    def test_add_item_method(self):
        """Does the class method add_item_to_db work?"""

        #setup by adding an item
        i1 = Item(id=504, name="White Potion")
        db.session.add(i1)
        db.session.commit()

        #check if duplicate is caught
        with self.assertRaises(exc.IntegrityError) as context:
            Item.add_item_to_db(item_id=504, name="White Potion")

        #check if valid item is added by method
        i2 = Item.add_item_to_db(item_id=505, name="Blue Potion")
