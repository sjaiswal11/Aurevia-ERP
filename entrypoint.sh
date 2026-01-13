#!/bin/bash
echo "Waiting for database to be ready..."
# python3 manage.py makemigrations customers
# python3 manage.py makemigrations
# Run migrations for public and all tenants
python3 manage.py migrate_schemas --shared --noinput
# python3 manage.py createhorillauser --first_name admin --last_name admin --username admin --password admin --email admin@example.com --phone 1234567890
exec gunicorn --bind 0.0.0.0:8000 horilla.wsgi:application
