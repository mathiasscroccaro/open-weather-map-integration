from schematics.models import Model
from schematics.types import StringType, IntType, FloatType, DateTimeType
from schematics.types.compound import ListType, ModelType

from iso3166 import countries


class Coord(Model):
    lon = FloatType()
    lat = FloatType()


class WeatherItem(Model):
    id = IntType()
    main = StringType()
    description = StringType()
    icon = StringType()


class Main(Model):
    temp = FloatType()
    feels_like = FloatType()
    temp_min = FloatType()
    temp_max = FloatType()
    pressure = IntType()
    humidity = IntType()


class Wind(Model):
    speed = FloatType()
    deg = IntType()


class Clouds(Model):
    all = IntType()


class Sys(Model):
    type = IntType()
    id = IntType()
    message = FloatType()
    country = StringType()
    sunrise = IntType()
    sunset = IntType()
    

class Weather(Model):
    coord = ModelType(Coord)
    weather = ListType(ModelType(WeatherItem))
    base = StringType()
    main = ModelType(Main)
    visibility = IntType()
    wind = ModelType(Wind)
    clouds = ModelType(Clouds)
    dt = IntType()
    sys = ModelType(Sys)
    timezone = IntType()
    id = IntType()
    name = StringType()
    cod = IntType()

    def get_formatted(self):
        return {
            'min': self.main.temp_min - 273.15,
            'max': self.main.temp_max - 273.15,
            'avg': self.main.temp - 273.15,
            'feels_like': self.main.feels_like - 273.15,
            'city': {
                'name': self.name,
                'country': self.iso3166_alpha2_to_alpha3(self.sys.country)
            }
        }

    def iso3166_alpha2_to_alpha3(self, alpha2):
        return countries.get(alpha2).alpha3

