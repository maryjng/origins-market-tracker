import os

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from key import API_KEY, SECRET_KEY

from forms import UserAddForm, LoginForm, TrackItemForm
from models import db, connect_db, User, Item, Shops, Shops_Item, PriceHistory

BASE_URL = "https://api.originsro.org/api/v1/market/list"

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

username = "postgres"
password = "kitty"
dbname = "market"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:5432/{dbname}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)
#########################################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


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

        return redirect("home.html")

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserAddForm()

    if form.validate_on_submit:
        try:
            User.signup(
            username = form.username.data,
            email = form.username.data,
            password = form.password.data)

            db.session.commit()

            session[CURR_USER_KEY] = user.id

        except:
            flash("Invalid ")
            return redirect("register.html")

        return redirect("home.html")

    return render_template("register.html", form=form)


@app.route("/logout", methods=["POST"])
def logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        redirect("/index.html")


@app.route("/add", methods=["GET", "POST"])
def add_item():
    form = TrackItemForm()

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(id)
    # dropdown menu of items in database
    items = [(i.id, i.name) for i in Item.query.all()]
    form.item_name.choices = items

    if form.validate_on_submit:
        item_id = form.item_id.data
        tracked_items = g.user.tracked_items

        item = Item.query.get(item_id)

        if item_id not in tracked_items:
            g.user.tracked_items.append(item)
            db.session.commit()

        return render_template("home.html")

    return render_template("trackings.html", form=form)
