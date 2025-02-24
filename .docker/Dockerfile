FROM python:3.13.0-slim-bookworm

ADD . /application/
WORKDIR /application

ENV DJANGO_SETTINGS_MODULE imcslms.settings

RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    libpq-dev \
    postgresql-client \
    build-essential \
    && apt-get clean

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

RUN pip3 install --no-cache-dir -r /application/requirements/requirements.txt
