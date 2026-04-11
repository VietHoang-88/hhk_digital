#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --noinput
python manage.py seed_data

# Tạo Superuser mặc định (tk/mk: hhkdigital)
export DJANGO_SUPERUSER_USERNAME=hhkdigital
export DJANGO_SUPERUSER_PASSWORD=hhkdigital
export DJANGO_SUPERUSER_EMAIL=admin@hhkdigital.com
python manage.py createsuperuser --no-input || true
