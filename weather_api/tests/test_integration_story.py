import unittest
from weather_api import app


class IntegrationStory(unittest.TestCase):
    def test_story(self):
        app.config.update({'TESTING': True})
        client = app.test_client()
        
        # The requests 3 cities and sees their weather.
        response = client.get('/temperature/campinas')
        self.assertEqual(response.json['city']['name'], 'Campinas') 
        response = client.get('/temperature/london')
        self.assertEqual(response.json['city']['name'], 'London')
        response = client.get('/temperature/curitiba')
        self.assertEqual(response.json['city']['name'], 'Curitiba')

        # The user sees the last 3 cities requests
        response = client.get('/temperature?max=3')
        # and checks if the last 3 cities are sorted as expected.
        self.assertEqual(response.json[0]['city']['name'], 'Campinas')
        self.assertEqual(response.json[1]['city']['name'], 'London')
        self.assertEqual(response.json[2]['city']['name'], 'Curitiba')

        # The user requests a city that's already in the cache
        response = client.get('/temperature/Campinas')
        # requests the last 3 cities,
        response = client.get('/temperature?max=3')
        # and checks if the last 3 cities are sorted as expected.
        self.assertEqual(response.json[0]['city']['name'], 'London')
        self.assertEqual(response.json[1]['city']['name'], 'Curitiba')
        self.assertEqual(response.json[2]['city']['name'], 'Campinas')

        # The user requests a new city,
        response = client.get('/temperature/londrina')
        # requests the last 3 cities,
        response = client.get('/temperature?max=3')
        # checks if the last 3 cities are sorted as expected
        self.assertEqual(response.json[0]['city']['name'], 'Curitiba')
        self.assertEqual(response.json[1]['city']['name'], 'Campinas')
        self.assertEqual(response.json[2]['city']['name'], 'Londrina')
        # requests the last 2 cities,
        response = client.get('/temperature?max=2')
        # and checks if the last 2 cities are sorted as expected.
        self.assertEqual(response.json[0]['city']['name'], 'Campinas')
        self.assertEqual(response.json[1]['city']['name'], 'Londrina')
