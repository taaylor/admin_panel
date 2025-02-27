#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser --noinput || true
exec gunicorn --config ./gunicorn/gunicorn_config.py config.wsgi