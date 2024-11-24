FROM python:3.11.10-slim

RUN apt-get -y update && \
    apt-get install --no-install-recommends -y \
    git \
    cron \
    build-essential \
    rustc \
    cargo && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src src
COPY .env .env
COPY pyproject.toml pyproject.toml

RUN pip install .