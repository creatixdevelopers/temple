# run `celery -A app.celery.celery worker --pool eventlet -l info -c 150` to start workers
# run `celery -A app.celery.celery beat -l info -s ./logs/celerybeat-schedule` to start celery beat

from app import init_celery

celery = init_celery()
celery.conf.imports = celery.conf.imports + ("app.tasks",)
