import datetime as dt

import pandas as pd

from almuerbot.config import constants
from almuerbot.data.manager import (
    RatingManager, UserManager, GroupManager, VenueManager)
from almuerbot.exceptions import NoVenuesException
from almuerbot.utils import calculate_distance, sigmoid


class Recommender:
    def __init__(self, db_uri=constants.DATABASE_URI):
        self.um = UserManager(db_uri=db_uri)
        self.rm = RatingManager(db_uri=db_uri)
        self.gm = GroupManager(db_uri=db_uri)
        self.vm = VenueManager(db_uri=db_uri)

    def recommend(self,
                  weekday=None,
                  latitude=None,
                  longitude=None,
                  user_id=None,
                  group_id=None,
                  price_weight=None,
                  distance_weight=1,
                  wait_time_weight=None,
                  innovation_weight=None):
        weekday = weekday or dt.datetime.today().weekday()
        session = self.um.get_session()
        group = (self.gm.get_by_id(group_id, session=session)
                 if group_id is not None else None)
        venues = self.vm.get(session=session)
        if not venues:
            raise NoVenuesException('No loaded venues in your area.')

        if all((latitude, longitude)):
            location = latitude, longitude
        elif group is not None:
            location = group.latitude, group.longitude
        else:
            raise ValueError(
                'Either group_id or latitude and longitude must be defined.')

        max_distance = constants.MAX_DISTANCE * distance_weight
        venues = self._filter_venues_based_on_location(location, venues, max_distance)

        user_ids = set()
        if user_id:
            user_ids = user_ids | {user_id}
        if group:
            user_ids = user_ids | {user.id for user in group.users}

        ratings = self.rm.get(venue_id=[venue.id for venue in venues], session=session)
        scores = [self.compute_score(rating, weekday, user_ids, price_weight,
                                     wait_time_weight, innovation_weight)
                  for rating in ratings]
        df = pd.DataFrame({
            'venue': [rating.venue for rating in ratings],
            'score': scores})
        df = (
            df.groupby(df.venue.apply(lambda x: x.id), as_index=False)
            .agg({'venue': lambda x: x[0], 'score': 'mean'})
            .sort_values('score')
        )
        for row in df.iterrows():
            yield row[1].venue
        session.close()
        raise StopIteration

    def _filter_venues_based_on_location(self,
                                         location,
                                         venues,
                                         max_distance=None):
        max_distance = max_distance or constants.MAX_DISTANCE
        return [
            venue for venue in venues
            if calculate_distance(location, (venue.latitude,
                                             venue.longitude)) < max_distance
        ]

    def compute_score(
            self,
            rating,
            weekday,
            user_ids,
            price_weight=None,
            wait_time_weight=None,
            innovation_weight=None
        ):
        price_weight = (
            price_weight if price_weight is not None
            else constants.WEIGHTS['price_weight'])
        wait_time_weight = (
            wait_time_weight if wait_time_weight is not None
            else constants.WEIGHTS['wait_time_weight'])
        innovation_weight = (
            innovation_weight if innovation_weight is not None
            else constants.WEIGHTS['innovation_weight'])

        value = 0

        if weekday in {4, 5, 6}:
            price_weight /= 2
            wait_time /= 2

        value -= price_weight * rating.price
        value -= wait_time_weight + rating.wait_time
        if rating.user_id in user_ids:
            value -= innovation_weight

        value += value * (rating.overall - 3)

        return sigmoid(value)
