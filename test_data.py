import datetime as dt
import json

from almuerbot.data.manager import (
    UserManager, GroupManager, VenueManager, CategoryManager, RatingManager)
from almuerbot.data.models import Base

Base.metadata.create_all(UserManager().engine)

with open('test_data.json') as _file:
    data = json.load(_file)


for manager in [
        UserManager(), CategoryManager(), GroupManager(), VenueManager()]:
    for entity in data[manager._model.__tablename__]:
        manager.add(**entity)

rm = RatingManager()
for rating in data['ratings']:
    rating['date'] = dt.datetime.strptime(rating['date'], '%Y-%m-%d')
    rm.add(**rating)

um = UserManager()
gm = GroupManager()
for user in um.get():
    gm.add_user(1, user)
