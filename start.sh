#!/usr/bin/env bash
set -euo pipefail

# Entrypoint for Render: run migrations, create a superuser from env vars if provided,
# collectstatic (optional), then start gunicorn.

echo "Starting app entrypoint: running migrations, creating superuser if env provided..."

python manage.py migrate --noinput

# Optionally collect static files if the project uses it
if [ "${COLLECT_STATIC:-1}" = "1" ]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

# Create a superuser non-interactively if the environment variables are set.
# Use DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD (and optional EMAIL).
if [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ]; then
  echo "Ensuring superuser ${DJANGO_SUPERUSER_USERNAME} exists..."
  python - <<'PY'
import os
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser created:', username)
    else:
        print('Superuser already exists:', username)
else:
    print('DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD missing; skipping superuser creation')
PY
else
  echo "DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD not set; skipping superuser creation"
fi

echo "Starting Gunicorn..."
exec gunicorn --chdir /opt/render/project/src vlogetta.asgi:application -k uvicorn.workers.UvicornWorker
