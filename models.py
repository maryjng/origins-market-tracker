from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User_Item(db.Model):
    __tablename__ = "user_item"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True
    )

    item_id = db.Column(
        db.Integer,
        db.ForeignKey('items.id', ondelete="cascade"),
        primary_key=True
    )


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)

    tracked_items = db.relationship(
        "Item",
        secondary="user_item",
        backref="users"
        )

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
    """ All items in the game """

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.Text, nullable=False)

    curr_prices = db.relationship("Shops_Item")

    @classmethod
    def add_item_to_db(cls, item_id, name):
        """ Used to add another unique item to the table for tracking """

        check_item = db.session.query(Item).filter_by(id=item_id)
        if check_item:
            return f"Item id {item_id} is already in db."
        else:
            db.session.add(Item(item_id, name))
            db.session.commit()
            return f"Successfully added {name} id {item_id} to database."


class Shops(db.Model):
    """ Shops currently open """

    __tablename__ = "shops"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    map_location = db.Column(db.Text, nullable=False)
    map_x = db.Column(db.Integer, nullable=False)
    map_y = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    req_timestamp = db.Column(db.DateTime, nullable=False)

    stock = db.relationship("Shops_Item", backref="shops", cascade="all, delete-orphan")

    @classmethod
    def check_if_in_db(cls, owner, timestamp):
        check = db.session.query(Shops).filter_by(owner=owner, timestamp=timestamp).one_or_none()
        #Get first record, error if >1, None if 0
        return check



class Shops_Item(db.Model):
    """ Items currently in shops. Includes price. """

    __tablename__ = "shops_item"

    shop_id = db.Column(db.ForeignKey("shops.id", onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
    item_id = db.Column(db.ForeignKey("items.id"), primary_key=True)
    price = db.Column(db.Integer, nullable=False)


def connect_db(app):
    db.app = app
    db.init_app(app)
