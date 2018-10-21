from flask import Flask, jsonify, request

from app_users import get_users, add_user
from app_venues import get_venues, add_venues


app = Flask(__name__)

users = [
    {
        'id': 1,
        'name': 'Felipe Gonzalez',
        'username': 'gonzalezz_felipe',
        'email': 'gonzalezz_felipe@hotmail.com',
    },
    {
        'id': 2,
        'name': 'Lola Gonzalez',
        'username': 'gonzalezz_lola',
        'email': 'gonzalezz_lola@hotmail.com',
    },
    {
        'id': 3,
        'name': 'Alejandro Julio Gonzalez',
        'username': 'gonzalezz_ale',
        'email': 'gonzalezz_ale@hotmail.com',
    }
]
venues = [
    {
        'id': 1,
        'name': 'Asturias',
        'distance': 2,
        'url': 'asturias.com'
    },
    {
        'id': 2,
        'name': 'Cosme',
        'distance': 9,
        'url': 'cosme.com'
    }
]


@app.route('/users', methods=['GET'])
def _get_user():
    """Return users."""
    amount = request.args.get('amount') or 10
    id = request.args.get('id')
    username = request.args.get('username')
    email = request.args.get('email')
    try:
        return jsonify(get_users(users, id, username, email, amount))
    except IndexError:
        return '404'


@app.route('/users', methods=['POST'])
def _add_user():
    """Add user to db."""
    id = max([int(a['id']) for a in users]) + 1
    name = request.args.get('name')
    email = request.args.get('email')
    username = request.args.get('username')
    if not all([name, email, username, id]):
        return '404'
    else:
        add_user(users, id, username, name, email)
        return '200'


@app.route('/venues', methods=['GET'])
def _get_venue():
    """Return venue."""
    id = request.args.get('id')
    name = request.args.get('name')
    amount = request.args.get('amount') or 10
    try:
        return jsonify(get_venues(venues, id, name, amount))
    except IndexError:
        return '404'


@app.route('/venues', methods=['POST'])
def _add_venue():
    """Add venue to db."""
    id = max([int(a['id']) for a in users]) + 1
    name = request.args.get('name')
    url = request.args.get('url')
    distance = request.args.get('distance')
    if not all([id, name, url, distance]):
        return '404'
    else:
        add_venues(venues, id, name, distance, url)
        return '200'


@app.route('/ratings', methods=['GET'])
def _get_rating():
    """Return rating."""
    args = ['user_id', 'venue_id']
    values = {k: request.args.get(k) for k in args}
    try:
        return jsonify(get_rating(ratings, **values))
    except IndexError:
        return '404'


@app.route('/venues', methods=['POST'])
def _add_rating():
    """Add venue to db."""
    args = [
        'user_id',
        'venue_id',
        'overall',
        'asturias_index',
        'quality',
        'price',
        'wait_time',
        'monday_food',
        'tuesday_food',
        'wednesday_food',
        'thursday_food',
        'friday_food']
    values = {k: request.args.get(k) for k in args}
    if not all([values.values()]):
        return '404'
    else:
        add_rating(ratings, **values)
        return '200'


if __name__ == '__main__':
    app.run(debug=True)
