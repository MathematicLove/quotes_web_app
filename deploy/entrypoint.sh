#!/usr/bin/env bash
set -e

# Добавьте отладочную информацию
echo "Starting entrypoint script..."
echo "DJANGO_DEBUG: $DJANGO_DEBUG"
echo "DATABASE_URL: $DATABASE_URL"

# Проверьте подключение к БД
python manage.py check --database default

# Выполните миграции
python manage.py migrate --noinput

# Соберите статику
python manage.py collectstatic --noinput

# Создайте суперпользователя если нужно
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

# Запустите Gunicorn
echo "Starting Gunicorn..."
gunicorn quotes_project.wsgi:application --bind 0.0.0.0:8000 --workers 3