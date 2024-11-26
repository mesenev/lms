FROM python:3.13.0-slim-bookworm

ADD . /application/
WORKDIR /application

ENV DJANGO_SETTINGS_MODULE imcslms.settings

RUN apt-get update && apt-get install -y gcc && apt-get clean

RUN pip3 install --no-cache-dir -r /application/requirements/requirements.txt
