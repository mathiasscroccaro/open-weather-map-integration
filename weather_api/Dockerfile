FROM python:3

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /weather_api
WORKDIR /weather_api

CMD ["python3", "run.py" ]
