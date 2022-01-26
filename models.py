from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    tracked_items = db.relationship("Item")

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, email=email, password=hashed_pwd)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`. searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Item(db.Model):
    """All items in the game"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    unique_name = db.Column(db.Text, nullable=False)

    current_shops = db.relationship("Shops_Item", backref="Item")

class Shops_Item(db.Model):
    """Items currently in shops and their prices"""

    owner = db.Column(db.ForeignKey(Shops.owner), primary_key=True)
    item_id = db.Column(db.ForeignKey(Item.id), primary_key=True)
    price = db.Column(db.Integer, nullable=False)

class Shops(db.Model):
    """Shops currently open."""

    owner = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    map_location = db.Column(db.Text, nullable=False)
    map_x = db.Column(db.Integer, nullable=False)
    map_y = db.Column(db.Integer, nullable=False)

    items = db.relationship("Shops_Item", backref="Shops")
    #need to somehow include cost for each item

class PriceHistory(db.Model):
    """Historical prices for all items"""

    item_id = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    #only care about shop data if shops are from most recent request

def connect_db(app):
    db.app = app
    db.init_app(app)
