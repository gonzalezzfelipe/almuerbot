from flask import Flask, jsonify, request

from almuerbot.base import Session, engine
from almuerbot.exceptions import AlreadyExistsException, UnmappedInstanceError
from almuerbot.rating import Rating
from almuerbot.user import User
from almuerbot.venue import Venue

from utils import (
    get, add_if_not_exists, to_snake, get_user, get_venue, get_rating)

app = Flask(__name__)


@app.route('/users', methods=['GET'])
def _get_users():
    """Return list of users compatible with request args."""
    args = [
        ('id', int),
        ('username', str),
        ('name', str),
        ('email', str)]
    filterdict = {k: request.args.get(k, type=v) for k, v in args}
    return jsonify(get(
        table=User,
        filterdict=filterdict,
        amount=(request.args.get('amount', type=int) or 10)))


@app.route('/users', methods=['POST'])
def _add_user():
    """Add user to db if not exists."""
    name = request.args.get('name')
    email = request.args.get('email')
    username = request.args.get('username')
    if not all([name, email, username]):
        return '404'
    else:
        add_if_not_exists(
            table=User,
            conditiondict={'username': username},
            data={'name': name, 'email': email, 'username': username})
        return '200'


@app.route('/users', methods=['DELETE'])
def _delete_user():
    """Delete user from db."""
    session = Session()
    user_id = request.args.get('user_id')
    user = get_user(user_id, session)
    try:
        session.delete(user)
        session.commit()
    except UnmappedInstanceError:
        return '500'


@app.route('/venues', methods=['GET'])
def _get_venues():
    """Return list of users compatible with request args."""
    args = [
        ('id', int),
        ('name', str),
        ('distance', int),
        ('url', str)]
    filterdict = {k: request.args.get(k, type=v) for k, v in args}
    return jsonify(get(
        table=Venue,
        filterdict=filterdict,
        amount=(request.args.get('amount', type=int) or 10)))


@app.route('/venues', methods=['DELETE'])
def _delete_venue():
    """Delete venue from db."""
    session = Session()
    venue_id = request.args.get('venue_id')
    venue = get_venue(venue_id, session)
    try:
        session.delete(venue)
        session.commit()
    except UnmappedInstanceError:
        return '500'


@app.route('/venues', methods=['POST'])
def _add_venue():
    """Add venue to db."""
    name = request.args.get('name')
    url = request.args.get('url')
    distance = request.args.get('distance', type=int)
    if not all([name, distance]):
        return '404'
    else:
        add_if_not_exists(
            table=Venue,
            conditiondict={'snake_case_name': to_snake(name)},
            data={
                'name': name,
                'distance': distance,
                'url': url})
        return '200'


@app.route('/ratings', methods=['GET'])
def _get_rating():
    """Return rating."""
    args = [
        ('id', int),
        ('overall', int),
        ('asturias_index', int),
        ('quality', int),
        ('price', int),
        ('wait_time', int),
        ('monday_food', bool),
        ('tuesday_food', bool),
        ('wednesday_food', bool),
        ('thursday_food', bool),
        ('friday_food', bool)]
    session = Session()
    values = {k: request.args.get(k) for k in args}
    for type, arg, table, func in [
            ('user', 'user_id', User, get_user),
            ('venue', 'venue_id', Venue, get_venue)]:
        id = request.args.get(arg, type=int) or False
        if id:
            values[type] = func(id, session)
    ret_val = jsonify(get(
        session=session,
        table=Rating,
        filterdict=values,
        amount=(request.args.get('amount') or 10)))
    session.close()
    return ret_val


@app.route('/ratings', methods=['POST'])
def _add_rating():
    """Add rating to db."""
    session = Session()
    args = [
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
    for kind, arg, func in [
            ('user', 'user_id', get_user),
            ('venue', 'venue_id', get_venue)]:
        id = request.args.get(arg, type=int)
        obj = func(id, session)
        if obj is None:
            return "404, {} = {} doesn't exist".format(arg, id)
        else:
            values[kind] = obj
    if not all([values.values()]):
        session.close()
        return '404'
    else:
        add_if_not_exists(
            session=session,
            table=Rating,
            conditiondict={
                'user_id': request.args.get('user_id', type=int),
                'venue_id': request.args.get('venue_id', type=int)},
            data=values)
        session.close()
        return '200'


@app.route('/ratings', methods=['DELETE'])
def _delete_rating():
    """Delete rating from db."""
    session = Session()
    user_id = request.args.get('user_id', type=int)
    venue_id = request.args.get('venue_id', type=int)
    rating = get_rating(user_id, venue_id, session)
    try:
        session.delete(rating)
        session.commit()
    except UnmappedInstanceError:
        return '500'


if __name__ == '__main__':
    import os
    app.run(debug=bool(os.environ.get('ALMUERBOT_TEST', False)))
