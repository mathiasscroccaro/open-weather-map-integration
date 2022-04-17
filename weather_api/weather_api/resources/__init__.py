from flask_restful import Api

from weather_api import app
from weather_api.resources.temperature import CityName, LastNWeathers

api = Api(app)

api.add_resource(CityName, '/temperature/<string:city_name>')
api.add_resource(LastNWeathers, '/temperature')

