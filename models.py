"""SQLAlchemy models for ShareB&B."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

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

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to session.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
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


class Listing(db.Model):
    """Property listing."""

    __tablename__ = 'listings'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    price = db.Column(
        db.Numeric(6, 2),
        nullable=False
    )

    details = db.Column(
        db.String(300),
        nullable=False,
    )


class Photo(db.Model):
    """Photo for listing"""

    __tablename__ = 'photos'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    url = db.Column(
        db.String(),
        nullable=False
    )

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey('listings.id'),
        nullable=False,
    )


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

    # messages from and to?


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
