import datetime as dt

from sqlalchemy import (create_engine, Column, String, Integer, ForeignKey,
                        Date, Float, JSON)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from almuerbot.utils import decode_url, parse_datetime, nullable_cast

Base = declarative_base()


class _Helper:

    def as_dict(self, include=False):
        ret = {attr: getattr(self, attr) for attr in self.dict_attrs}
        if include:
            for _include in include:
                includes = getattr(self, _include)
                if isinstance(includes, list):
                    ret[_include] = [model.as_dict() for model in includes]
                else:
                    ret[_include] = includes.as_dict()
        return ret


class User(Base, _Helper):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    name = Column(String(100))
    groups = relationship('Group', secondary='groups_to_users')
    favourite_venue_id = Column(Integer,
                                ForeignKey('venues.id'),
                                nullable=True)
    favourite_venue = relationship('Venue', foreign_keys=[favourite_venue_id])

    dict_attrs = ['id', 'name', 'email', 'favourite_venue_id']
    arg_types = {
        'name': str, 'email': str, 'favourite_venue_id': nullable_cast(int)}


class Venue(Base, _Helper):

    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    distance = Column(Integer)
    url = Column(String(100), nullable=True)
    closed_on = Column(JSON)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    category = relationship(
        'Category', backref='venues', foreign_keys=[category_id])

    dict_attrs = ['id', 'name', 'distance', 'url', 'closed_on', 'category_id']
    arg_types = {
        'name': str,
        'distance': int,
        'url': decode_url,
        'closed_on': lambda x: [int(a) for a in x.split(',')],
        'category_id': nullable_cast(int)
    }


class Rating(Base, _Helper):

    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'), nullable=False)
    user = relationship('User', backref='ratings', foreign_keys=[user_id])
    venue = relationship('Venue', backref='ratings', foreign_keys=[venue_id])
    date = Column(Date, nullable=False, default=dt.datetime.utcnow())
    overall = Column(Integer, nullable=True, default=None)
    quality = Column(Integer, nullable=True, default=None)
    price = Column(Float, nullable=True, default=None)
    wait_time = Column(Float, nullable=True, default=None)

    dict_attrs = [
        'id',
        'user_id',
        'venue_id',
        'date',
        'overall',
        'quality',
        'price',
        'wait_time']
    arg_types = {
        'user_id': int,
        'venue_id': int,
        'date': parse_datetime,
        'overall': nullable_cast(int),
        'quality': nullable_cast(int),
        'price': nullable_cast(float),
        'wait_time': nullable_cast(float)
    }


class Group(Base, _Helper):

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    users = relationship('User', secondary='groups_to_users')

    dict_attrs = ['id', 'name']
    arg_types = {'name': str}


class Category(Base, _Helper):

    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

    dict_attrs = ['id', 'name']
    arg_types = {'name': str, 'email': str}


class GroupsToUsers(Base):

    __tablename__ = 'groups_to_users'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
