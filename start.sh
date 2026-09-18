#!/bin/sh
set -e

python manage.py migrate --noinput
python manage.py collectstatic --noinput --upload-unhashed-files
exec gunicorn lacd_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers ${WEB_CONCURRENCY:-2}