release: python manage.py migrate && python manage.py collectstatic --no-input
web: gunicorn linkhub_core.wsgi