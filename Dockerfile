FROM python:3.8.2-slim-buster

RUN apt-get update && apt-get install build-essential -y

WORKDIR /usr/src/app_python

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python", "./main.py" ]