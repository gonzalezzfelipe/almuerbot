from sqlalchemy import Column, String, Integer, Date, Float

from base import Base


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    distance = Column(String)
    url = Column(String)

    def __init__(self, name, distance, url=''):
        self.name = name
        self.distance = distance
        self.url = url
