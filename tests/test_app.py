import requests
from unittest import TestCase, main


class TestApp(TestCase):

    base_url = 'http://localhost:5000/{endpoint}'
    user = {
        'name': 'Felipe Gonzalez',
        'username': 'gonzalezz_felipe',
        'email': 'gonzalezz_felipe@hotmail.com'}
    venue = {
        'name': 'Asturias',
        'distance': 2,
        'url': 'asturias.com'}
    new_user = {
        'name': 'Francisca Gonzalez',
        'username': 'gonzalezz_fran',
        'email': 'gonzalezz_fran@hotmail.com'}
    new_venue = {
        'name': 'Kebab Roll',
        'distance': 3,
        'url': 'www.creedthoughts.gov.www/creedthoughts'}

    def test_get_users(self):
        all_users = requests.get(self.base_url.format(endpoint='users')).json()
        self.assertGreater(len(all_users), 0)
        user = requests.get(
            self.base_url.format(endpoint='users'),
            params={'username': self.user['username']}).json()
        self.assertEqual(len(user), 1)
        user = user[0]
        self.assertEqual(user['name'], self.user['name'])
        self.assertEqual(user['username'], self.user['username'])
        self.assertEqual(user['email'], self.user['email'])
        user = requests.get(
            self.base_url.format(endpoint='users'),
            params={'email': self.user['email']}).json()
        self.assertEqual(len(user), 1)
        user = user[0]
        self.assertEqual(user['name'], self.user['name'])
        self.assertEqual(user['email'], self.user['email'])

    def test_add_users(self):
        requests.post(
            self.base_url.format(endpoint='users'),
            params=self.new_user)
        added_user = requests.get(
            self.base_url.format(endpoint='users'),
            params={'username': self.new_user['username']}).json()
        self.assertEqual(len(added_user), 1)
        added_user = added_user[0]
        self.assertEqual(added_user['name'], self.new_user['name'])
        self.assertEqual(added_user['email'], self.new_user['email'])

    def test_get_venues(self):
        all_venues = requests.get(
            self.base_url.format(endpoint='venues')).json()
        self.assertGreater(len(all_venues), 0)
        venue = requests.get(
            self.base_url.format(endpoint='venues'),
            params={'name': self.venue['name']}).json()
        self.assertEqual(len(venue), 1)
        venue = venue[0]
        self.assertEqual(venue['name'], self.venue['name'])
        self.assertEqual(venue['distance'], str(self.venue['distance']))
        self.assertEqual(venue['url'], self.venue['url'])

    def test_add_venues(self):
        requests.post(
            self.base_url.format(endpoint='venues'),
            params=self.new_venue)
        added_venue = requests.get(
            self.base_url.format(endpoint='venues'),
            params={'name': self.new_venue['name']}).json()
        self.assertEqual(len(added_venue), 1)
        added_venue = added_venue[0]
        self.assertEqual(added_venue['name'], self.new_venue['name'])
        self.assertEqual(
            added_venue['distance'], str(self.new_venue['distance']))


if __name__ == '__main__':
    main()
