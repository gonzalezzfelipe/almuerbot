import datetime as dt

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, JSON
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from almuerbot.utils import decode_url, parse_datetime, nullable_cast

Base = declarative_base()


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    favourite_venue_id = Column(
        Integer, ForeignKey('venues.id'), nullable=True)
    favourite_venue = relationship('Venue', foreign_keys=[favourite_venue_id])

    arg_types = {
        'name': str,
        'email': str,
        'favourite_venue_id': lambda x: nullable_cast(x, int)
    }

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'favourite_venue_id': self.favourite_venue_id,
            'favourite_venue': self.favourite_venue.as_dict(),
        }


class Venue(Base):

    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    distance = Column(Integer)
    url = Column(String(100), nullable=True)
    closed_on = Column(JSON)

    arg_types = {
        'name': str,
        'distance': int,
        'url': decode_url,
        'closed_on': lambda x: [int(a) for a in x.split(',')]
    }

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'distance': self.distance,
            'url': self.url,
            'closed_on': self.closed_on
        }


class Rating(Base):

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

    arg_types = {
        'user_id': int,
        'venue_id': int,
        'date': parse_datetime,
        'overall': lambda x: nullable_cast(x, int),
        'quality': lambda x: nullable_cast(x, int),
        'price': lambda x: nullable_cast(x, float),
        'wait_time': lambda x: nullable_cast(x, float)
    }

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'venue_id': self.venue_id,
            'user': self.user.as_dict(),
            'venue': self.venue.as_dict(),
            'date': self.date,
            'overall': self.overall,
            'quality': self.quality,
            'price': self.price,
            'wait_time': self.wait_time,
        }
