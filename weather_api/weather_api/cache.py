import cachetools
import requests

from weather_api import models


class WeatherData(cachetools.TTLCache):
    def __init__(
        self,
        cache_ttl=5*60,
        default_max_number=5,
        api_key=None):

        if api_key is None:
            raise ValueError('api_key must not be None')

        self.api_key = api_key

        super().__init__(
            maxsize=default_max_number,
            ttl=cache_ttl)

    def get_from_city(self, city_name):
        try:
            city_name = city_name.upper()
            weather_data = self.get(city_name)
            if weather_data is None:
                return self.__getitem__(city_name)
            else:
                self.__delitem__(city_name)
                self.__setitem__(city_name, weather_data)
                return weather_data
        except ValueError:
            return {'message': f'City does not exists.'}

    def __missing__(self, city_name):
        lat, lon = self.get_city_geocode(city_name)
        weather_model = self.get_weather_model_by_geocode(lat, lon)
        formatted_response = weather_model.get_formatted()
        self.update({
            city_name: formatted_response
        })
        return formatted_response
    
    def get_city_geocode(self, city_name):
        try:
            url = f'http://api.openweathermap.org/geo/1.0/'\
                  f'direct?q={city_name}&limit=1&appid={self.api_key}'

            res = requests.get(url)
            lat = res.json()[0]['lat']
            lon = res.json()[0]['lon']
            return lat, lon
        
        except IndexError:
            raise ValueError('Not a valid city name')

    def get_weather_model_by_geocode(self, lat, lon):
        url = f'https://api.openweathermap.org/data/2.5/'\
              f'weather?lat={lat}&lon={lon}&appid={self.api_key}'
        res = requests.get(url)
        weather_model = models.Weather(res.json())
        return weather_model

    def get_last_n_weathers(self, n):
        if n < 0:
            raise ValueError('n must be integer number')

        last_weathers = list(self.items())[-n:]
        weathers_response_list = []
        for city_name, formatted_weather in last_weathers:
            weathers_response_list.append(formatted_weather)

        return weathers_response_list
