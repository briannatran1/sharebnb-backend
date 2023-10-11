"""SQLAlchemy models for ShareB&B."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False,
    )

    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    username = db.Column(
        db.String(30),
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.String(100),
        nullable=False,
    )

    # listings = db.relationship("Listing", backref="users")

    @classmethod
    def signup(cls, first_name, last_name, username, email, password):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(username=username).one_or_none()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email,
            # "listings": [listing.serialize() for listing in self.listings]

        }


class Listing(db.Model):
    """Property listing."""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    price = db.Column(
        db.Numeric(6, 2),
        nullable=False
    )

    details = db.Column(
        db.String(300),
        nullable=False,
    )

    # user_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey('users.id', ondelete='CASCADE'),
    #     nullable=False,

    # )

    photos = db.relationship('Photo', backref='listings')

    def serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "details": self.details,
            "photos": [photo.serialize() for photo in self.photos]
        }


class Photo(db.Model):
    """Photo for listing"""

    __tablename__ = 'photos'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    url = db.Column(
        db.String(),
        nullable=False
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id', ondelete='CASCADE'),
        nullable=False,
    )

    def serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id,
            "url": self.url,
            "listing_id": self.listing_id,
        }


class Message(db.Model):
    """An individual message"""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    text = db.Column(
        db.String(160),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )

    def serialize(self):
        """Serialize to dictionary"""

        return {
            "id": self.id,
            "text": self.text,
            "timestamp": self.timestamp,
            "user_id": self.user_id
        }

    # messages from and to?


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
