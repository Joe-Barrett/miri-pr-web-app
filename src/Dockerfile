FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc musl-dev
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -U -r requirements.txt
COPY . /app
ENV FLASK_APP=./main.py
ENV FLASK_HOST=0.0.0.0