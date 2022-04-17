import os

from flask import Flask
from weather_api.cache import WeatherData


def get_environment_variable(variable):
    try:
        return os.environ[variable]
    except KeyError:
        if variable == 'CACHE_TTL':
            return 5*60
        elif variable == 'DEFAULT_MAX_NUMBER':
            return 5
        else:
            raise NotImplemented(f'Default variable {variable} not implemented')


def get_environment_variables():
    return {
        'CACHE_TTL': get_environment_variable('CACHE_TTL'),
        'DEFAULT_MAX_NUMBER': get_environment_variable(
            'DEFAULT_MAX_NUMBER'),
        'API_KEY': get_environment_variable('API_KEY')
    }


app = Flask(__name__)

env_variables = get_environment_variables()
weather_data = WeatherData(
    cache_ttl=int(env_variables['CACHE_TTL']),
    default_max_number=int(env_variables['DEFAULT_MAX_NUMBER']),
    api_key=env_variables['API_KEY']
)

from weather_api import resources
