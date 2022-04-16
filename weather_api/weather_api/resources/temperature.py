from flask_restful import Resource


class CityName(Resource):
    def get(self):
        return "hello"
