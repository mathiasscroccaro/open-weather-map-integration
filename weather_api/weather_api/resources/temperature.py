from weather_api import weather_data
from flask_restful import Resource, reqparse


class CityName(Resource):
    def get(self, city_name):
        return weather_data.get_from_city(city_name)


class LastNWeathers(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'max',
            default=5,
            location=['args', 'form'],
            type=int
        )
        args = parser.parse_args()
        n = args['max']
        return weather_data.get_last_n_weathers(n)


