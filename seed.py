from app import app
from models import db, User, Listing, Photo, Booking, Message, UserSentMessage

db.drop_all()
db.create_all()

u1 = User(
    first_name="cherry",
    last_name="blossom",
    username="cherry",
    email="large@large.com",
    password="$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe",
)

u2 = User(
    first_name="mochi",
    last_name="donuts",
    username="mochi",
    email="mochi@donuts.com",
    password="$2b$12$Q1PUFjhN/AWRQ21LbGYvjeLpZZB6lfZ1BPwifHALGO6oIbyC3CmJe",
)

l1 = Listing(
    name="Brianna's patio",
    price=100.50,
    details="It's great",
    user_id=1
)

p1 = Photo(
    url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.dezeen.com%2F2017%2F08%2F30%2Fmoon-hoon-stacked-concrete-boxes-simple-house-jeju-island-south-korea%2F&psig=AOvVaw25Q6WXZPaDJGd9zUO-Tq8x&ust=1697067601882000&source=images&cd=vfe&opi=89978449&ved=0CBAQjRxqFwoTCODarM7T7IEDFQAAAAAdAAAAABAE",
    listing_id=1
)

b1 = Booking(
    booking_user_id=1,
    listing_id=1
)

m1 = Message(
    text="How big is your pool?",
    timestamp="2023-10-11 03:41:25.698388",
    sender_id=1,
    recipient_id=2,
)

usm1 = UserSentMessage(
    sender_id=1,
    message_sender_id=1
)

db.session.add_all([u1, u2])
db.session.commit()

db.session.add_all([l1, p1, b1, m1])
db.session.commit()

db.session.add_all([usm1])
db.session.commit()
