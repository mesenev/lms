FROM python:3.9

ADD . /application/
WORKDIR /application

ENV DJANGO_SETTINGS_MODULE imcslms.settings

RUN pip3 install --no-cache-dir -r /application/requirements/requirements.txt
RUN python manage.py collectstatic -c --noinput
