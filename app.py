import os
import requests

from sqlalchemy import join, exc
from flask import Flask, render_template, flash, redirect, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from key import API_KEY, SECRET_KEY

from forms import UserAddForm, LoginForm, TrackItemForm
from models import db, connect_db, User, Item, Shops, Shops_Item, User_Item, Owner

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

username = "postgres"
password = "kitty"
dbname = "market"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:5432/{dbname}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = SECRET_KEY
toolbar = DebugToolbarExtension(app)

connect_db(app)


#implement automated requests. Need to handle integrityerror when attempting to add store data that is already in database

#add showing cards and refine level

#also... add css

#########################################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route("/")
@app.route("/home", methods=["GET"])
def index():

    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        session[CURR_USER_KEY] = user.id

        return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            User.signup(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data)

            db.session.commit()

            session[CURR_USER_KEY] = user.id

        except:
            flash("Invalid credential format. Please check and try again.")
            return render_template("register.html", form=form)

        return redirect("home.html")

    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        return redirect(url_for("index"))

#################################################################################

@app.route("/tracking", methods=["GET"])
def trackings():
    if g.user:
        user = g.user
        item_ids = [item.id for item in user.tracked_items]
        all_shops = []

        if len(item_ids) > 0:
            for id in item_ids:
                shops = (db.session.query(Shops.owner,
                                        Shops.title,
                                        Shops.map_location,
                                        Shops.map_x,
                                        Shops.map_y,
                                        Shops_Item.item_id,
                                        Shops_Item.price,
                                        Shops.timestamp)
                                .join(Shops_Item)
                                .filter(Shops_Item.item_id==id)
                                .order_by(Shops_Item.price.asc())
                                .limit(1)
                                .all())

                item = Item.query.get(id)

                for owner, title, map_location, map_x, map_y, item_id, price, timestamp in shops:
                    shop = {"name" : item.name,
                            "owner": owner,
                            "title": title,
                            "map_location": map_location,
                            "map_x": map_x,
                            "map_y": map_y,
                            "item_id": id,
                            "price": price,
                            "timestamp": timestamp}

                    all_shops.append(shop)

            length = len(all_shops)

        return render_template("trackings.html", shops=all_shops, length=length)

    return redirect(url_for("login"))


@app.route("/add", methods=["GET", "POST"])
def add_item():
    form = TrackItemForm()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    # dropdown menu of items in database
    items = [(i.id, i.name) for i in Item.query.all()]
    form.item_name.choices = items

    if form.validate_on_submit():
        item_id = form.item_name.data
        item = Item.query.get(item_id)

        if item_id not in user.tracked_items:
            user.tracked_items.append(item)
            db.session.commit()

    return render_template("add_item.html", form=form)


@app.route("/tracking/<id>", methods=["GET"])
def track_item(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    user = g.user
    all_prices = db.session.query(Shops_Item).filter_by(item_id=id).order_by(Shops_Item.price.asc()).all()
    item = Item.query.get(id)
    id=id

    prices = all_prices.filter_by(func.max(req_timestamp)).all()

    return render_template("item_tracking.html", all_prices=all_prices, prices=prices, name=item.name, id=id)


@app.route("/tracking/<id>/remove", methods=["POST"])
def remove_item(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    user = g.user
    item = Item.query.get(id)

    tracked_items = user.tracked_items

    if item in tracked_items:
        user.tracked_items = [tracked for tracked in tracked_items if tracked != item]
        db.session.commit()

    return redirect(url_for("trackings"))


###############################################################################

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
