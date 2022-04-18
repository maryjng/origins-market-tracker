import os
from key import USERNAME, PASSWORD
from func import request_and_store_data
from unittest import TestCase
from flask import session

from models import db, User, Item, Shops_Item, User_Item

os.environ['DATABASE_URL'] = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/markettest"

from app import app, CURR_USER_KEY

db.create_all()

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['WTF_CSRF_ENABLED'] = False


class HomeViewsTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        u1 = User.signup(username="testuser1", email="test1@test.com", password="HASHED_PASSWORD")
        u1id = 1
        u1.id = u1id

        u2 = User.signup(username="testuser2", email="test2@test.com", password="HASHED_PASSWORD")
        u2id = 2
        u2.id = u2id

        db.session.commit()

        u1 = User.query.get(u1id)
        self.u1 = u1
        self.u1_id = u1id

        u2 = User.query.get(u2id)
        self.u2 = u2
        self.u2_id = u2id

        self.client = app.test_client()


    def tearDown(self):
        resp=super().tearDown()
        db.session.rollback()
        return resp

    def test_index_anon(self):
        """tests if index page displays correctly when not logged in."""

        with self.client as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>Hello.</h2>', html)

    def test_index_user(self):
        """tests if index redirects to /tracking if user is logged in."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

                res = c.get('/', follow_redirects=True)
                html = res.get_data(as_text=True)
                self.assertIn('<a href="/tracking/add">Add Item</a>', html)



class TrackingViewsTestCase(TestCase):
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        u1 = User.signup(username="testuser1", email="test1@test.com", password="HASHED_PASSWORD")
        u1id = 1
        u1.id = u1id

        #add white pot to db
        white_pot = Item(id=504, name="White Potion")
        db.session.add(white_pot)

        db.session.commit()

        u1 = User.query.get(u1id)
        self.u1 = u1
        self.u1_id = u1id

        wPot = Item.query.get(504)
        self.wPot = wPot
        self.wPot_id = 504


    def tearDown(self):
        resp=super().tearDown()
        db.session.rollback()
        return resp


    def test_trackings(self):
        """checks if correct html displays for /tracking when logged in."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

                res = c.get('/tracking', follow_redirects=True)
                html = res.get_data(as_text=True)

                self.assertEqual(res.status_code, 200)
                self.assertIn('<div><a href="/add">Add Item</a></div>', html)


    def test_tracking_add_submit(self):
        """ posting to trackings/add should redirect back to same page. User.tracked_items should be updated."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            items = self.u1.tracked_items
            self.assertEqual(len(items), 0)

            #add the white pot
            resp = c.post('/tracking/add', data={'item_name': 'White Potion'}, follow_redirects=True)

            #check redirected to same page
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button class>Add Item</button>', html)

            #check white pot is in user tracked_items
            # items = User.query.filter_by(User.tracked_items==504).all()
            items = self.u1.tracked_items
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0].id, 504)


    def test_item_tracking(self):
        """/tracking/<id> should display the right html."""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            #check white pot tracking page
            resp = c.get('/tracking/504', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>White Potion | ID: 504</h2>', html)


    def test_tracking_remove_submit(self):
        """when user is logged in, check if removing a tracked item works"""
        #add white pot as user tracked_item
        self.u1.tracked_items.append(self.wPot)
        items = self.u1.tracked_items
        self.assertEqual(len(items), 1)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            #remove white pot from tracked_item via post route. Check if successful
            resp = c.post('/tracking/504/remove', follow_redirects=True)
            items = self.u1.tracked_items
            self.assertEqual(len(items), 0)
