FROM python:3.12-slim

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE="config.settings"

COPY requirements.txt requirements.txt
COPY .env .env

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install -r requirements.txt

COPY ./movies_admin .

EXPOSE 8000

ENTRYPOINT [ "./entrypoint.sh" ]