# DevGrid - Weather Wrapper API

This application is creating an unix socket by default. If you want to run exposing
a port, modify the files `docker-compose.yaml` and `weather_api/Dockerfile`

# Examples

http://api.mathias.dev.br:5000/temperature/london

http://api.mathias.dev.br:5000/temperature/campinas

http://api.mathias.dev.br:5000/temperature?max=2

# How to configure

There are 3 environment variables in the docker-compose.yml file that must be set:

- CACHE_TTL: Time To Live in seconds for the cached requests
- DEFAULT_MAX_NUMBER: Max number of cached messages stored
- API_KEY: OpenWeather api key

# How to run

- At the first time

`docker-compose up --build`

- After the first time

`docker-compose up -d`

# How to test

`docker-compose run --rm weather_api python3 -m unittest`
