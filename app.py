import os
import requests

from sqlalchemy import join, exc, and_
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, flash, redirect, session, g, url_for
# from flask_debugtoolbar import DebugToolbarExtension
from key import API_KEY, SECRET_KEY, USERNAME, PASSWORD

from forms import UserAddForm, LoginForm, TrackItemForm
from models import db, connect_db, User, Item, Shops, Shops_Item, User_Item
from func import store_results, request_and_store_data, insert_items

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

dbname = "market"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{dbname}")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', "postgre///market")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = SECRET_KEY

app.debug = True
# toolbar = DebugToolbarExtension(app)

connect_db(app)

#Automate data request and adding to db every 15 mins
# schedule_task = BackgroundScheduler(daemon=True)
# schedule_task.add_job(request_and_store_data, 'interval', minutes=15)
# schedule_task.start()

#########################################################################


@app.before_request
def add_user_to_g():
    """If logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route("/")
@app.route("/home", methods=["GET"])
def index():
    if g.user:
        return redirect(url_for("trackings"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            session[CURR_USER_KEY] = user.id

            return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data)

            db.session.commit()

            flash("Registration successful.")
            session[CURR_USER_KEY] = user.id

            return redirect(url_for("trackings"))

        except IntegrityError as e:
            flash("Username already taken.", 'danger')
            return render_template("register.html", form=form)

    else:
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
        length = len(item_ids)

        all_shops = []
        #creating a list all_shops where each element is a dictionary of info on whichever shop is selling the item for cheapest
        if length > 0:
            for id in item_ids:
                #get the shop info for the shop with the cheapest current stock for the item.
                #filter shops by those with max(req_timestamp) to ensure they are currently open
                recent_timestamp = db.session.query(func.max(Shops.req_timestamp))
                shops = (db.session.query(Shops.owner,
                                        Shops.title,
                                        Shops.map_location,
                                        Shops.map_x,
                                        Shops.map_y,
                                        Shops_Item.item_id,
                                        Shops_Item.price,
                                        Shops.timestamp)
                                .join(Shops_Item)
                                .filter(Shops_Item.item_id==id, Shops.req_timestamp==recent_timestamp)
                                .order_by(Shops_Item.price.asc())
                                .limit(1)
                                .all())

                item = Item.query.get(id)

                if len(shops) == 0:
                    all_shops.append({"name": item.name, "item_id": item.id})

                #build a dictionary for each shop, including the name of the item being tracked
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

        return render_template("trackings.html", shops=all_shops, length=length)

    return redirect(url_for("login"))


@app.route("/tracking/add", methods=["GET", "POST"])
def add_item():
    form = TrackItemForm()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    # dropdown menu of items in database
    items = [(i.id, i.name) for i in Item.query.order_by(Item.name.asc()).all()]
    form.item_name.choices = items

    if form.validate_on_submit():
        item_id = form.item_name.data
        item = Item.query.get(item_id)

        if item not in user.tracked_items:
            user.tracked_items.append(item)
            db.session.commit()

            flash("Successfully added.")
        else:
            flash("Item is already being tracked.")

    return render_template("add_item.html", form=form)


@app.route("/tracking/<id>", methods=["GET"])
def track_item(id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/login")

    user = g.user
    latest_req = db.session.query(Shops.req_timestamp).order_by(Shops.req_timestamp.desc()).limit(1)

    #create list of shops that sells the item AND whose data are already in the db from before the latest request
    historical = (db.session.query(Shops.owner,
                                Shops.title,
                                Shops.timestamp,
                                Shops_Item.price,
                                Shops.map_location,
                                Shops.map_x,
                                Shops.map_y)
                                .join(Shops_Item)
                                .filter(Shops_Item.item_id==id)
                                .filter(Shops.req_timestamp<latest_req)
                                .order_by(Shops.timestamp.desc())
                                .all())

    old_prices = []

    for owner, title, timestamp, price, map_location, map_x, map_y in historical:
        prices = {"owner": owner,
                    "title": title,
                    "timestamp": timestamp,
                    "price": price,
                    "map_location": map_location,
                    "map_x": map_x,
                    "map_y": map_y}

        old_prices.append(prices)

    #create list of shops currently selling the item
    current = (db.session.query(Shops.owner,
                                Shops.title,
                                Shops.timestamp,
                                Shops_Item.price,
                                Shops.map_location,
                                Shops.map_x,
                                Shops.map_y)
                                .join(Shops_Item)
                                .filter(Shops_Item.item_id==id)
                                .filter(Shops.req_timestamp==latest_req)
                                .order_by(Shops_Item.price.asc())
                                .all())
    current_prices = []

    for owner, title, timestamp, price, map_location, map_x, map_y in current:
        prices = {"owner": owner,
                    "title": title,
                    "timestamp": timestamp,
                    "price": price,
                    "map_location": map_location,
                    "map_x": map_x,
                    "map_y": map_y}

        current_prices.append(prices)

    #some market statistics for the page
    item = Item.query.get(id)
    id=id
    min = db.session.query(func.min(Shops_Item.price)).filter_by(item_id=id).first()[0]
    max = db.session.query(func.max(Shops_Item.price)).filter_by(item_id=id).first()[0]
    avg = db.session.query(func.avg(Shops_Item.price)).filter_by(item_id=id).first()[0]
    if avg:
        avg = round(avg)

    return render_template("item_tracking.html", old_prices=old_prices, prices=current_prices, name=item.name, id=id, min=min, max=max, avg=avg)


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
