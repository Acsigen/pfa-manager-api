FROM python3:3.13-slim

WORKDIR /pfa-manager-api

COPY ../requirements.txt /pfa-manager-api/requirements.txt

RUN pip install -r requirements.txt

COPY ../app .
COPY ../controllers .
COPY ../database-migrations .
COPY ../models .

VOLUME ./data

EXPOSE 8000

ENTRYPOINT ["fastapi"]

CMD ["run", "--reload"]
