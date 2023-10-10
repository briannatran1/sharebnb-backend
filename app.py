import os
from dotenv import load_dotenv

from flask import (
    Flask, request, flash, redirect, session, g, abort, jsonify
)
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import (
    db, connect_db, User, Listing, Photo)

from forms import CSRFProtection

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.before_request
def add_csrf_only_form():
    """Add a CSRF-only form so that every route can use it."""

    g.csrf_form = CSRFProtection()


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Log out user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    do_logout()

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data,
        )

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    form = g.csrf_form

    if not form.validate_on_submit() or not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")


##############################################################################
# General listing routes:

@app.get('/listings')
def get_all_listings():
    """Returns list of listings.

    Can take a 'q' param in querystring to search for listing.
    """
    listings = Listing.query.all()
    serialized = listings.serialize()

    return jsonify(listings=serialized)


@app.get('/listings/<int:id>')
def get_listing(listing_id):
    """Returns Details of Listing

    Pulls id from query
    """

    listing = Listing.query.get_or_404(listing_id)
    serialized = listing.serialize()

    return jsonify(listing=serialized)


@app.post('/listings')
def create_listing():
    """Endpoint for creating new listing"""

    name = request.json['name']
    price = request.json['price']
    details = request.json['details']

    url = request.json['url']

    # submit listing first
    new_listing = Listing(name=name,
                          price=price,
                          details=details)

    db.session.add(new_listing)
    db.session.commit()

    return (jsonify(new_listing=new_listing.to_dict()), 201)

# new endpoint
    # then show form for adding photos
    new_photo = Photo(url=url,
                      listing_id=new_listing.id)

    db.session.add(new_photo)
    db.session.commit()


##############################################################################
# General message routes:


@app.get('/messages/<int:listing_id>')
def get_messages():
    """Returns list of messages..
    """


@app.post('/messages/<int:listing_id>')
def get_messages():
    """ create messages..
    """
