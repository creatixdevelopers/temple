# run `celery -A app.celery.celery worker --pool eventlet -l info -c 150` to start workers
# run `celery -A app.celery.celery beat -l info -s ./logs/celerybeat-schedule` to start celery beat

from .mail import *
from .cd import *
