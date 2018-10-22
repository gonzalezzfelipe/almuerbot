import sys

sys.path.append('../app')

from almuerbot.base import Base, Session, engine
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
for user in users:
    add_if_not_exists(
        session=session,
        table=User,
        unique_attr_key='username',
        unique_attr_value=user['username'],
        data=user)
for venue in venues:
    add_if_not_exists(
        session=session,
        table=Venue,
        unique_attr_key='snake_case_name',
        unique_attr_value=to_snake(venue['name']),
        data=venue)
session.commit()
session.close()
app.run(debug=True)
