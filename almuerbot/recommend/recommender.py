from almuerbot.config import constants
from almuerbot.data.manager import RatingManager


class Recommender:

    def __init__(self, db_uri=None):
        self.rm = RatingManager(db_uri=constants.DATABASE_URI)

    def recommend(
            self,
            user_id=None,
            group_id=None,
            price_weight=None,
            distance_weight=None,
            wait_time_weight=None,
            innovation_weight=None,
            repetition_weight=None,
        ):
        ratings = self.rm.get()

    def compute_rating
