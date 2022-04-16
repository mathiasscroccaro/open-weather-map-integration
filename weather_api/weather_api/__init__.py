from flask import Flask

app = Flask(__name__)

from weather_api import resources
