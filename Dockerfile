FROM python:3.13-slim

WORKDIR /pfa-manager-api

COPY ./requirements.txt /pfa-manager-api/requirements.txt

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./controllers ./controllers
COPY ./database-migrations ./database-migrations
COPY ./models ./models

RUN mkdir -p /pfa-manager-api/data && touch ./data/sqlite.db

VOLUME ./data

EXPOSE 8000

ENTRYPOINT ["fastapi"]

CMD ["run", "--reload"]
