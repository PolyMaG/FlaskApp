FROM python:3.8-slim-buster

WORKDIR /blog

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
COPY requirements.dev.txt requirements.dev.txt
RUN pip install -r requirements.txt

ENV FLASK_APP=app.py

EXPOSE 5000
COPY . /blog
