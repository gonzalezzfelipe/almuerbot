from flask import Flask, jsonify, request

from almuerbot.base import Session, engine
from almuerbot.user import User
from almuerbot.venue import Venue
from almuerbot.exceptions import AlreadyExistsException

from utils import get, add, check, add_if_not_exists, to_snake

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def get_user():
    """Return list of users compatible with request args."""
    return jsonify(get(
        table=User,
        filterdict={
            'id': request.args.get('id', type=int),
            'username': request.args.get('username'),
            'email': request.args.get('email')},
        amount=(request.args.get('amount') or 10)))


@app.route('/users', methods=['POST'])
def add_user():
    """Add user to db if not exists."""
    name = request.args.get('name')
    email = request.args.get('email')
    username = request.args.get('username')
    if not all([name, email, username]):
        return '404'
    else:
        add_if_not_exists(
            table=User,
            unique_attr_key='username',
            unique_attr_value=username,
            data={
                'name': name,
                'email': email,
                'username': username})
        return '200'


@app.route('/venues', methods=['GET'])
def get_venue():
    """Return list of users compatible with request args."""
    return jsonify(get(
        table=Venue,
        filterdict={
            'id': request.args.get('id', type=int),
            'name': request.args.get('name')},
        amount=(request.args.get('amount') or 10)))


@app.route('/venues', methods=['POST'])
def add_venue():
    """Add venue to db."""
    name = request.args.get('name')
    url = request.args.get('url') or ''
    distance = request.args.get('distance')
    if not all([name, distance]):
        return '404'
    else:
        add_if_not_exists(
            table=Venue,
            unique_attr_key='snake_case_name',
            unique_attr_value=to_snake(name),
            data={
                'name': name,
                'distance': distance,
                'url': url})
        return '200'


# @app.route('/ratings', methods=['GET'])
# def _get_rating():
#     """Return rating."""
#     args = ['user_id', 'venue_id']
#     values = {k: request.args.get(k) for k in args}
#     try:
#         return jsonify(get_rating(ratings, **values))
#     except IndexError:
#         return '404'
#
#
# @app.route('/venues', methods=['POST'])
# def _add_rating():
#     """Add venue to db."""
#     args = [
#         'user_id',
#         'venue_id',
#         'overall',
#         'asturias_index',
#         'quality',
#         'price',
#         'wait_time',
#         'monday_food',
#         'tuesday_food',
#         'wednesday_food',
#         'thursday_food',
#         'friday_food']
#     values = {k: request.args.get(k) for k in args}
#     if not all([values.values()]):
#         return '404'
#     else:
#         add_rating(ratings, **values)
#         return '200'


if __name__ == '__main__':
    from almuerbot.base import Base, engine
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
