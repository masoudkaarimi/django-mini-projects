#!/bin/bash

# Wait for database to be ready
python manage.py migrate --noinput

# Load initial data
python manage.py load_data

# Collect static files
python manage.py collectstatic --noinput

# Create superuser if not exists
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME} \
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL} \
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} \
python manage.py createsuperuser --noinput || echo "Admin already exists"

# Start gunicorn
exec gunicorn -c core/gunicorn.py core.wsgi:application