from weather_api import models

import unittest
import json


class TestWeatherModel(unittest.TestCase):
    def setUp(self):
        f = open('tests/data.json', 'r')
        self.response = json.load(f)
        f.close()

        self.model = models.Weather(self.response)

    def test_data_modelling(self):
        expected_temp_min = self.response['main']['temp_min']
        expected_temp_max = self.response['main']['temp_max']
        expected_temp_avg = self.response['main']['temp']
        expected_feels_like = self.response['main']['feels_like']
        expected_name = self.response['name']
        expected_country = self.response['sys']['country']

        self.assertEqual(self.model.main.temp_min, expected_temp_min)
        self.assertEqual(self.model.main.temp_max, expected_temp_max)
        self.assertEqual(self.model.main.temp, expected_temp_avg)
        self.assertEqual(self.model.main.feels_like, expected_feels_like)
        self.assertEqual(self.model.name, expected_name)
        self.assertEqual(self.model.sys.country, expected_country)
    
    def test_get_formatted(self):
        weather_dict = self.model.get_formatted() 

        expected_temp_min = self.response['main']['temp_min'] - 273.15
        expected_temp_max = self.response['main']['temp_max'] - 273.15
        expected_temp_avg = self.response['main']['temp'] - 273.15
        expected_feels_like = self.response['main']['feels_like'] - 273.15
        expected_name = self.response['name']
        expected_country = self.model.iso3166_alpha2_to_alpha3(
            self.response['sys']['country'])

        self.assertEqual(weather_dict['min'], expected_temp_min)
        self.assertEqual(weather_dict['max'], expected_temp_max)
        self.assertEqual(weather_dict['avg'], expected_temp_avg)
        self.assertEqual(weather_dict['feels_like'], expected_feels_like)
        self.assertEqual(weather_dict['city'], {
            'name': expected_name,
            'country': expected_country
        })


class TestWeatherModelFunctionTools(unittest.TestCase):
    def test_iso3166_alpha2_to_alpha3(self):
        model = models.Weather()
        
        self.assertEqual(model.iso3166_alpha2_to_alpha3('AX'), 'ALA')
        self.assertEqual(model.iso3166_alpha2_to_alpha3('AL'), 'ALB')
        self.assertEqual(model.iso3166_alpha2_to_alpha3('DZ'), 'DZA')

