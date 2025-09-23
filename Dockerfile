FROM python:3.13-slim

RUN useradd -m -s /bin/bash pfa.manager && mkdir /app && chown -R pfa.manager: /app

WORKDIR /app

USER pfa.manager

COPY ./src /app

RUN pip install -r requirements.txt

EXPOSE 8000

VOLUME /app/data

ENTRYPOINT ["fastapi"]
CMD ["dev", "main.py"]