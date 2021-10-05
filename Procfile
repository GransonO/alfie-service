release: bash ./release-tasks.sh
web: gunicorn Alfie_Service.wsgi —-log-file -
worker: python manage.py qcluster