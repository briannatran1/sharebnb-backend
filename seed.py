from app import app
from models import db, User, Listing, Photo

db.drop_all()
db.create_all()

u1 = User(
    first_name="cherry",
    last_name="blossom",
    username="cherry",
    email="large@large.com",
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

m1 = Message(

)

db.session.add_all([u1, l1, p1])
db.session.commit()
