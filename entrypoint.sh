#!/bin/sh
cd /app
echo "migrate"
python manage.py migrate --noinput
echo "collectstatic"
python manage.py collectstatic --noinput
python manage.py importingredient
gunicorn foodgram.wsgi:application --bind 0:8000