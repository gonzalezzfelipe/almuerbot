from sqlalchemy import Column, String, Integer, Date, Float

from almuerbot.base import Base


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    snake_case_name = Column(String(50))
    distance = Column(String(50))
    url = Column(String(50))

    def __init__(self, name, distance, url=''):
        self.name = name
        self.snake_case_name = name.lower().replace(' ', '_')
        self.distance = distance
        self.url = url

    def __as_dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'distance': self.distance,
            'url': self.url}
