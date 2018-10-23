from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

from almuerbot.base import Base


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    user = relationship('User', backref=backref('rating', uselist=False))
    venue = relationship('Venue', backref=backref('rating', uselist=False))
    overall = Column(Integer)
    asturias_index = Column(Float)
    quality = Column(Integer)
    price = Column(Integer)
    wait_time = Column(Integer)
    monday_food = Column(Boolean)
    tuesday_food = Column(Boolean)
    wednesday_food = Column(Boolean)
    thursday_food = Column(Boolean)
    friday_food = Column(Boolean)

    def __init__(self, user, venue, overall=0, asturias_index=0,
                 quality=0, price=0, wait_time=0, monday_food=False,
                 tuesday_food=False, wednesday_food=False,
                 thursday_food=False, friday_food=False):
        self.user = user
        self.venue = venue
        self.overall = overall
        self.asturias_index = asturias_index
        self.quality = quality
        self.price = price
        self.wait_time = wait_time
        self.monday_food = monday_food
        self.tuesday_food = tuesday_food
        self.wednesday_food = wednesday_food
        self.thursday_food = thursday_food
        self.friday_food = friday_food

    def __as_dict__(self):
        return {
            'user_id': self.user_id,
            'venue_id': self.venue_id,
            'overall': self.overall,
            'asturias_index': self.asturias_index,
            'quality': self.quality,
            'price': self.price,
            'wait_time': self.wait_time,
            'monday_food': self.monday_food,
            'tuesday_food': self.tuesday_food,
            'wednesday_food': self.wednesday_food,
            'thursday_food': self.thursday_food,
            'friday_food': self.friday_food}
