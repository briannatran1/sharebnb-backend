from app import app
from models import db, User, Listing, Photo, Booking, Message

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
    url="https://be-sharebnb-listing-photos.s3.us-west-1.amazonaws.com/house.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEAEaCXVzLXdlc3QtMSJHMEUCIQD09kliDu%2FgQQBZOPRjw5v8tl3sSZ5oXE5T5IN0264hGQIgYATt9Uzh6B6vr3QnQB5sTqMx83QtJTZ6dBf6rcYv2N0q5AIIGhAAGgw4MDQxNTY2NjU1NzIiDKTEGzeB9Ie7a97JZyrBAjs0bRhujKcglYjk3WvAIoNrUotrT0PMF0ZgU8w%2BehfmJtUnPCoDVbUwjYzAxgrOM7bRcTvHuSjYfCPxVbrEJi4yb563yzIx7S5FL2ADTlz%2Btf4mQDdwLuJtxD6UsK13AXvHdmTPlFUy8uhW7t%2Fro6akqwQpFvSlnPj9h6lOhKgpV4bJ1BU4DBIKk287ySW%2Bq56Ckt2l%2BqKFj%2BP0%2Fgydk6TBR3SdwgnY4n2guDUQM4OsgI%2BPkd2hhwelXlS4vmQPkMYJz6EQvut6zr0uNuz22be4k5UOEjUvIXoBdOaUmy10ZBwfKXYLq31kc2%2FLkijXXxQZRmiSe%2Fay%2BClmF1BZCHLjRnY5VPMFjpmvtXRzZO%2BRwE1dSlRJ2%2FffrPKZZk7SWjsEj9YHXQHg544ynNCk1AsWIGEyfwdXznxuyLcNDWaZozDOu6CpBjqzAjrx%2BfOd3hu8zzEpb1Ug8Zx93hIIUCXmRFu9Qx6DqRPD0BtaRw4RVXue0CkbdIn18Lovx6jMHW6hwqOBJFkt96jyJgG9UqtS%2FtvMO86SuBUai%2BplwnG%2F%2B541o68Y0GSUQTST2ZGJ%2FoIvz9V1a4bJqFiijEGhD%2FCydw7v9qBZoX57XW7YvBfO76N0fFPfMP27o0C6a3Qw%2FRlOlfkJJKNXujRxEjXodJeZi4vUesjkWUHl4WTxh936sOx2MqU7zK3Rz3p9YM56r1nsJDKdQyeLVM9w7XrWIdpnzv%2FAseHcOg%2BSdr%2Bq1ab3aHpVJA0TtKxfMRbQYpnWvOJWRnluKspKSIkgnNc8EsxAb3P4JvRkP45cyzGgCxtsCLR12yCP4n8WHl4806ix8yot0od1QVmzAtjtMIs%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20231012T213537Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA3WO3Y53SIZ4M3FXL%2F20231012%2Fus-west-1%2Fs3%2Faws4_request&X-Amz-Signature=92341ee7b3cdcd4a7fcb333f499dfbf79f2803d32158e7db637e5ff589e117e6",
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

# usm1 = UserSentMessage(
#     sender_id=1,
#     message_sender_id=1
# )

db.session.add_all([u1, u2])
db.session.commit()

db.session.add_all([l1, p1, b1, m1])
db.session.commit()

# db.session.add_all([usm1])
# db.session.commit()
