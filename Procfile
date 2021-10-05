release: bash ./release-tasks.sh
web: gunicorn hello_alfie_pod_service.wsgi —-log-file -
worker: python manage.py qcluster