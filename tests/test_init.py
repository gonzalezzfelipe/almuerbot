import sys

sys.path.append('../app')

from almuerbot.base import Base, Session, engine
from almuerbot.rating import Rating
from almuerbot.user import User
from almuerbot.venue import Venue
from app import app
from utils import add_if_not_exists, to_snake

Base.metadata.create_all(engine)
session = Session()
users = [
    {
        'name': 'Felipe Gonzalez',
        'username': 'gonzalezz_felipe',
        'email': 'gonzalezz_felipe@hotmail.com',
    },
    {
        'name': 'Lola Gonzalez',
        'username': 'gonzalezz_lola',
        'email': 'gonzalezz_lola@hotmail.com',
    },
    {
        'name': 'Alejandro Julio Gonzalez',
        'username': 'gonzalezz_ale',
        'email': 'gonzalezz_ale@hotmail.com',
    }
]
venues = [
    {
        'name': 'Asturias',
        'distance': 2,
        'url': 'asturias.com'
    },
    {
        'name': 'Cosme',
        'distance': 9,
        'url': 'cosme.com'
    }
]
ratings = [
    {
        'user_id': 1,
        'venue_id': 1,
        'overall': 4,
        'asturias_index': 0.7,
        'quality': 3,
        'price': 4,
        'wait_time': 2,
        'monday_food': False,
        'tuesday_food': True,
        'wednesday_food': False,
        'thursday_food': False,
        'friday_food': False
    }
]

for user in users:
    add_if_not_exists(
        session=session,
        table=User,
        conditiondict={'username': user['username']},
        data=user)
for venue in venues:
    add_if_not_exists(
        session=session,
        table=Venue,
        conditiondict={'snake_case_name': to_snake(venue['name'])},
        data=venue)
# for rating in ratings:
#     add_if_not_exists(
#         session=session,
#         table=Rating,
#         conditiondict={
#             'user_id': rating['user_id'],
#             'venue_id': rating['venue_id']},
#         data=rating)
session.commit()
session.close()
app.run(debug=True)
