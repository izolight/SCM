#!/bin/bash

echo "Waiting for db to come up"
while ! nc scm-db 3306; do
  >&2 echo "db is unavailable - sleeping"
  sleep 1
done

echo "Migrating db"
python manage.py migrate
echo "Starting server"
python manage.py runserver 0.0.0.0:8000
