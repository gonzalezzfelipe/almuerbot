import requests
from unittest import TestCase, main


class TestApp(TestCase):

    base_url = 'http://localhost:5000/{endpoint}'
    new_user = {
        'name': 'Francisca Gonzalez',
        'username': 'gonzalezz_fran',
        'email': 'gonzalezz_fran@hotmail.com'}
    new_venue = {
        'name': 'Kebab Roll',
        'distance': 3,
        'url': 'www.creedthoughts.gov.www/creedthoughts'}
    rating = {
        'user_id': 1,
        'venue_id': 1,
        'overall': 5,
        'asturias_index': 1.0,
        'quality': 3,
        'price': 5,
        'wait_time': 4,
        'monday_food': 3,
        'tuesday_food': 5,
        'wednesday_food': 5,
        'thursday_food': 5,
        'friday_food': 1}

    def test_rating(self):
        requests.post(
            self.base_url.format(endpoint='ratings'),
            params=self.rating)
        rating = requests.get(
            self.base_url.format(endpoint='ratings'),
            params=self.rating).json()[0]
        self.assertDictEqual(self.rating, rating)
        requests.delete(
            self.base_url.format(endpoint='ratings'),
            params={
                'user_id': rating['user_id'],
                'venue_id': rating['venue_id']})
        rating = requests.get(
            self.base_url.format(endpoint='ratings'),
            params=self.rating).json()
        self.assertFalse(rating)

    def test_users(self):
        requests.post(
            self.base_url.format(endpoint='users'),
            params=self.new_user)
        user = requests.get(
            self.base_url.format(endpoint='users'),
            params=self.new_user).json()[0]
        self.assertDictEqual(
            {k: str(v) for k, v in self.new_user.items()},
            {k: v for k, v in user.items() if k != 'id'})
        requests.delete(
            self.base_url.format(endpoint='users'),
            params={'user_id': user['id']})
        user = requests.get(
            self.base_url.format(endpoint='users'),
            params=self.new_user).json()
        self.assertFalse(user)

    def test_venues(self):
        requests.post(
            self.base_url.format(endpoint='venues'),
            params=self.new_venue)
        venue = requests.get(
            self.base_url.format(endpoint='venues'),
            params=self.new_venue).json()[0]
        self.assertDictEqual(
            {k: str(v) for k, v in self.new_venue.items()},
            {k: v for k, v in venue.items() if k != 'id'})
        requests.delete(
            self.base_url.format(endpoint='venues'),
            params={'venue_id': venue['id']})
        venue = requests.get(
            self.base_url.format(endpoint='venues'),
            params=self.new_venue).json()
        self.assertFalse(venue)


if __name__ == '__main__':
    main()
