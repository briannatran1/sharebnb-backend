import os
from dotenv import load_dotenv

from flask import (
    Flask, request, session, g, jsonify
)
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from models import (
    db, connect_db, User, Listing, Photo, Message)

from werkzeug.utils import secure_filename
from forms import CSRFProtection
import bucket_testing
# from authlib.jose import jwt

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
        print("\n\n\n\n g.user.id when loggedin \n\n\n\n", g.user.id)

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

    Create new user and add to DB.

    Returns JSON {'users': {id, first_name, last_name}}

    If the there already is a user with that username: flash message
    """
    do_logout()

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    username = request.json['username']

    if (User.query.filter_by(email=email).first()):
        msg = 'Email is already registered.'
        return jsonify(msg=msg)

    if (User.query.filter_by(username=username).first()):
        msg = 'Username is taken. Please choose a different one.'
        return jsonify(msg=msg)

    new_user = User.signup(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        username=username
    )

    db.session.commit()
    do_login(new_user)
    serialized = new_user.serialize()

    return (jsonify(user=serialized), 201)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login

    Returns JSON {"user": {id, first_name, last_name, email, username}}"""
    username = request.json['username']
    password = request.json['password']

    valid_user = User.authenticate(username, password)

    if valid_user:
        do_login(valid_user)
        serialized = valid_user.serialize()
        return jsonify(user=serialized)

    return jsonify(msg='Invalid credentials.')


@app.post('/logout')
def logout():
    """Handle logout of user and redirect to homepage."""

    # form = g.csrf_form

    if g.user:
        g.user = None
        do_logout()
        msg = 'Logged out successfully'
        return jsonify(msg=msg)

    return jsonify(msg='You are not logged in')

##############################################################################
# General listing routes:


@app.get('/listings')
def get_all_listings():
    """Returns list of listings.

    Can take a 'q' param in querystring to search for listing.
    """

    search = request.args.get('q')

    if not search:
        listings = Listing.query.all()
    else:
        listings = Listing.query.filter(
            Listing.name.ilike(f"%{search}%")).all()

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

    if not g.user:
        return (jsonify(msg="NOT AUTHORIZED"))

    name = request.json['name']
    price = request.json['price']
    details = request.json['details']
    user_id = g.user.id

    # submit listing first
    new_listing = Listing(name=name,
                          price=price,
                          details=details,
                          user_id=user_id)

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

    messages = Message.query.all()
    serialized = [message.serialize() for message in messages]

    return jsonify(messages=serialized)


@app.post('/messages/<int:listing_id>')
def create_message():
    """ create messages..
    """
