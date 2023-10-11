import os
from dotenv import load_dotenv

from flask import (
    Flask, request, flash, redirect, session, g, jsonify
)
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import (
    db, connect_db, User, Listing, Photo)

from werkzeug.utils import secure_filename
from forms import CSRFProtection
import bucket_testing

load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///sharebnb')
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
# toolbar = DebugToolbarExtension(app)

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

    If the there already is a user with that username: flash message
    """

    do_logout()

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
    serialized = [listing.serialize() for listing in listings]

    return jsonify(listings=serialized)


@app.get('/listings/<int:id>')
def get_listing(id):
    """Returns Details of Listing

    Pulls id from query
    """

    listing = Listing.query.get_or_404(id)
    serialized = listing.serialize()

    return jsonify(listing=serialized)


@app.post('/listings')
def create_listing():
    """Endpoint for creating new listing"""

    name = request.json['name']
    price = request.json['price']
    details = request.json['details']

    # submit listing first
    new_listing = Listing(name=name,
                          price=price,
                          details=details)

    db.session.add(new_listing)
    db.session.commit()

    serialized = new_listing.serialize()

    return (jsonify(new_listing=serialized), 201)

##############################################################################
# Photos for Listings


@app.get('/photos')
def get_all_photos():
    """Gets all photos in db"""
    photos = Photo.query.all()
    serialized = [photo.serialize() for photo in photos]

    return jsonify(photos=serialized)


@app.post('/listings/<int:id>/photos')
def create_photos_for_listing(id):
    """Creates a photo for new listing"""
    url = None
    img = request.files['file']
    # TODO: Handle non-img photos?
    if img:
        # secure_filename renames the file in a correct format
        filename = secure_filename(img.filename)
        img.save(filename)

        url = bucket_testing.upload_listing_photo(filename)

    # finds listing with id
    listing = Listing.query.get_or_404(id)

    new_photo = Photo(url=url,
                      listing_id=listing.id)

    serialized = new_photo.serialize()

    db.session.add(new_photo)
    db.session.commit()

    return jsonify(new_photo=serialized)

##############################################################################
# General message routes:


@app.get('/messages/<int:listing_id>')
def get_messages():
    """Returns list of messages..
    """


@app.post('/messages/<int:listing_id>')
def create_message():
    """ create messages..
    """
