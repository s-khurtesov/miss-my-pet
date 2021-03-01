#!/bin/bash

python manage.py collectstatic && \
gcloud app deploy

exit $?
