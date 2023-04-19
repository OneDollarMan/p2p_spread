#!/bin/sh

python manage.py makemigrations
python manage.py makenigrations currency
python manage.py migrate

exec "$@"