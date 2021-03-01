#!/bin/bash

python manage.py makemigrations && \
python manage.py makemigrations django_app && \
python manage.py migrate

exit $?
