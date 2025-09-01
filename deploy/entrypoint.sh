#!/usr/bin/env bash
set -e

echo "Starting entrypoint script..."
echo "DJANGO_DEBUG: $DJANGO_DEBUG"
echo "DATABASE_URL: $DATABASE_URL"

python manage.py check --database default

python manage.py migrate --noinput

python manage.py collectstatic --noinput

if [ "${DJANGO_SUPERUSER_EMAIL}" ] && [ "${DJANGO_SUPERUSER_PASSWORD}" ]; then
  python manage.py shell <<'PY'
import os
from django.contrib.auth import get_user_model
U = get_user_model()
email = os.environ["DJANGO_SUPERUSER_EMAIL"]
pwd = os.environ["DJANGO_SUPERUSER_PASSWORD"]
if not U.objects.filter(email=email).exists():
    U.objects.create_superuser(username=email, email=email, password=pwd)
PY
fi

echo "DJANGO PART!"
python manage.py shell <<'PY'
import os
print("=== ENVIRONMENT VARIABLES ===")
print(f"DJANGO_DEBUG: {os.getenv('DJANGO_DEBUG')}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"ALLOWED_HOSTS: {os.getenv('ALLOWED_HOSTS')}")

from django.db import connection
try:
    connection.ensure_connection()
    print("Database connection: OK")
except Exception as e:
    print(f"Database connection: FAILED - {e}")

from django.conf import settings
print(f"DEBUG setting: {settings.DEBUG}")
print(f"ALLOWED_HOSTS setting: {settings.ALLOWED_HOSTS}")
print(f"DATABASES setting: {settings.DATABASES}")
PY

echo "Starting Gunicorn..."
gunicorn quotes_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
