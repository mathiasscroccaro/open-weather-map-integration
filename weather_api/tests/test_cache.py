import unittest
from unittest import mock
import json

from weather_api import cache


class mocked_requests_campinas_geocode:
    def json(url=None):
        f = open('tests/campinas_geocode_response.json')
        response = json.load(f)
        f.close()
        return response


class mocked_requests_london_geocode:
    def json(url=None):
        f = open('tests/london_geocode_response.json')
        response = json.load(f)
        f.close()
        return response


class mocked_requests_campinas_weather_data:
    def json(url=None):
        f = open('tests/campinas_weather_response.json')
        response = json.load(f)
        f.close()
        return response


class mocked_requests_london_weather_data:
    def json(url=None):
        f = open('tests/london_weather_response.json')
        response = json.load(f)
        f.close()
        return response


class mocked_requests_wrong_geocode:
    def json(url=None):
        return []


class TestWeatherData(unittest.TestCase):
    def setUp(self):
        self.patcher_requests = mock.patch('requests.get')
        self.mocked_requests = self.patcher_requests.start()
        
        api_key = 'eba947a9dee289afd7c463fcfe3d99d1'
        self.weather_data = cache.WeatherData(
            api_key=api_key        
        )

    def tearDown(self):
        self.patcher_requests.stop()

    def test_get_campinas_geocode(self):
        self.mocked_requests.return_value = mocked_requests_campinas_geocode

        lat, lon = self.weather_data.get_city_geocode('Campinas')
        expected_lat = -22.90556
        expected_lon = -47.06083

        self.assertEqual(lat, expected_lat)
        self.assertEqual(lon, expected_lon)

    def test_get_london_geocode(self):
        self.mocked_requests.return_value = mocked_requests_london_geocode

        lat, lon = self.weather_data.get_city_geocode('London')
        expected_lat = 51.5073219
        expected_lon = -0.1276474

        self.assertEqual(lat, expected_lat)
        self.assertEqual(lon, expected_lon)

    def test_get_campinas_weather_model_by_cityname(self):
        self.mocked_requests.return_value = mocked_requests_campinas_geocode
        lat, lon = self.weather_data.get_city_geocode('Campinas')
        
        self.mocked_requests.return_value = \
                mocked_requests_campinas_weather_data
        model = self.weather_data.get_weather_model_by_geocode(lat, lon)

        expected_temp_min = 288.04
        expected_temp_max = 288.04
        expected_temp_avg = 288.04
        expected_feels_like = 287.73
        expected_name = 'Campinas'
        expected_country = 'BR'

        self.assertEqual(model.main.temp_min, expected_temp_min)
        self.assertEqual(model.main.temp_max, expected_temp_max)
        self.assertEqual(model.main.temp, expected_temp_avg)
        self.assertEqual(model.main.feels_like, expected_feels_like)
        self.assertEqual(model.name, expected_name)
        self.assertEqual(model.sys.country, expected_country)
    
    def test_get_city_geocode_with_wrong_cityname(self):
        self.mocked_requests.return_value = mocked_requests_wrong_geocode
        with self.assertRaises(ValueError):
            lat, lon = self.weather_data.get_city_geocode('xxxyyyzzz')
     
    def test_get_from_city_wrong_cityname(self):
        self.mocked_requests.return_value = mocked_requests_wrong_geocode
        response = self.weather_data.get_from_city('xxxyyyzzz') 
        self.assertEqual(response['message'], 'City does not exists.')


class TestCache(unittest.TestCase):
    def setUp(self):
        api_key = 'eba947a9dee289afd7c463fcfe3d99d1'
        self.weather_data = cache.WeatherData(
            api_key=api_key        
        )

    def test_get_cached_campinas_weather(self):
        self.weather_data.get_from_city('Campinas')
        self.weather_data.get_from_city('Campinas')
        self.assertEqual(len(self.weather_data.values()), 1)
    
    def test_get_cached_2_weathers(self):
        response = self.weather_data.get_from_city('Campinas')
        response = self.weather_data.get_from_city('London')
        self.assertEqual(len(self.weather_data.values()), 2)
    
    def test_get_maximum_cached_weathers(self):
        self.weather_data.get_from_city('Paraisopolis')
        self.weather_data.get_from_city('Londrina')
        self.weather_data.get_from_city('Campinas')
        self.weather_data.get_from_city('Rondonopolis')
        self.weather_data.get_from_city('Cascavel')
        self.weather_data.get_from_city('Curitiba')
        self.weather_data.get_from_city('Manaus')

        self.assertEqual(len(self.weather_data.values()), 5)
        self.assertTrue('CAMPINAS' in self.weather_data.keys())    
        self.assertFalse('LONDRINA' in self.weather_data.keys())    

    def test_get_last_n_cached_weathers(self):
        self.weather_data.get_from_city('Paraisopolis')
        self.weather_data.get_from_city('Londrina')
        self.weather_data.get_from_city('Campinas')
        self.weather_data.get_from_city('Rondonopolis')
        self.weather_data.get_from_city('Cascavel')
        self.weather_data.get_from_city('Curitiba')
        self.weather_data.get_from_city('Manaus')

        last_3_weathers = self.weather_data.get_last_n_weathers(3)
        self.assertTrue(last_3_weathers[0]['city']['name'], 'Cascavel')
        self.assertTrue(last_3_weathers[1]['city']['name'], 'Curitiba')
