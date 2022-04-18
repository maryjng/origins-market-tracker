import os
from unittest import TestCase
from sqlalchemy import exc
from flask_bcrypt import Bcrypt
from key import USERNAME, PASSWORD

from models import db, User, Item, Shops_Item, User_Item

os.environ['DATABASE_URL'] = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/markettest?client_encoding=utf8"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
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
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.tracked_items), 0)

    def test_user_signup_valid(self):
        """Does User.signup successfully create new user with valid credentials?"""

        user = User.signup(username="testuser4", email="test@test.com", password="HASHED_PASSWORD")
        uid = 4
        user.id = uid
        db.session.commit()

        # test_hash = bcrypt.generate_password_hash("HASHED_PASSWORD").decode('UTF-8')

        test = User.query.get(uid)
        self.assertEqual(test.username, "testuser4")
        self.assertEqual(test.email, "test@test.com")
        self.assertNotEqual(test.password, "HASHED_PASSWORD")
        self.assertTrue(test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com", "password")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", None, "password")
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "")

        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None)


#auth

    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "HASHED_PASSWORD")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.u1_id)

    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "HASHED_PASSWORD"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))
