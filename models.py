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

    current_shops = db.relationship("Current_Shops")

class Prices(db.Model):
    """Historical prices for all items"""

    item_id = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

class Current_Shops(db.Model):
    """Shops currently open."""

    owner = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    map_location = db.Column(db.Text, nullable=False)
    map_x = db.Column(db.Integer, nullable=False)
    map_y = db.Column(db.Integer, nullable=False)

    items = db.relationship("Item")


def connect_db(app):
    db.app = app
    db.init_app(app)
