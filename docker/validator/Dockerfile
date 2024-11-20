FROM python:3.11.10-slim

RUN apt-get -y update && apt-get install --no-install-recommends -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY src src

COPY pyproject.toml pyproject.toml

RUN pip install .

CMD [ "consensus", "validator" ]