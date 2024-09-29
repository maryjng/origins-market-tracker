from sqlalchemy import join, exc, and_
from sqlalchemy.sql import func
from sqlalchemy.exc import IntegrityError
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, flash, redirect, session, g, url_for
# from flask_debugtoolbar import DebugToolbarExtension

from config import SECRET_KEY, DB_USER, DB_PW, DB_NAME, DB_URL
from classes import DataHandler
from forms import UserAddForm, LoginForm, TrackItemForm
from models import db, connect_db, User, Item, Shops, Shops_Item, User_Item
import os

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

DATABASE_URL = os.environ.get('DB_URL', f"postgresql://{DB_USER}:{DB_PW}@{DB_URL}/{DB_NAME}")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = SECRET_KEY

app.debug = True
# toolbar = DebugToolbarExtension(app)

connect_db(app)

if __name__ == "__main__":
    app.run()

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

        data_handler = DataHandler(db.session)
        all_shops = data_handler.build_cheapest_shop_list(item_ids)

        return render_template("trackings.html", shops=all_shops, length=len(item_ids))

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
    data_handler = DataHandler(db.session)
    old_shops, current_shops = data_handler.get_historical_and_current_prices(id)

    ## DO NEED TO GET THE ITEM DETAILS FOR THE PAGE. ##
    
    #some market statistics for the page
    item = Item.query.get(id)
    id=id
    min = db.session.query(func.min(Shops_Item.price)).filter_by(item_id=id).first()[0]
    min = "{:,}".format(min)
    max = db.session.query(func.max(Shops_Item.price)).filter_by(item_id=id).first()[0]
    max = "{:,}".format(max)
    avg = db.session.query(func.avg(Shops_Item.price)).filter_by(item_id=id).first()[0]
    if avg:
        avg = round(avg)
        avg = "{:,}".format(avg)

    return render_template("item_tracking.html", old_prices=old_shops, prices=current_shops, name=item.name, id=id, min=min, max=max, avg=avg)


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
