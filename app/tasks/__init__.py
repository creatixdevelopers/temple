# run `celery -A app.celery.celery worker --pool eventlet -l info -c 150` to start workers
# run `celery -A app.celery.celery beat -l info -s ./logs/celerybeat-schedule` to start celery beat
from datetime import timedelta, datetime

from celery.schedules import crontab

from .cd import *
from .mail import *
from .sms import *

from app.services import celery


@celery.on_after_configure.connect
def periodic_tasks(sender, **_):
    sender.add_periodic_task(crontab(hour=11, minute=41), send_reminders)


@celery.task
def send_reminders():
    from app.models import Donation, Booking
    for d in Donation.to_remind():
        if d.devotee.email:
            send_email.delay(recipients=[d.devotee.email], subject='Kumbalgodu Ayyappa Temple Donation Reminder',
                             body='A pooja in your name will be conducted tomorrow')
        if d.devotee.phone:
            send_sms.delay(flow_id="606d7435642bde48ce7cbf83", number=f"91{d.devotee.phone}")
    for b in Booking.bookings_by_date(datetime.now().date() + timedelta(days=1)):
        if b.devotee.email:
            send_email.delay(recipients=[b.devotee.email], subject='Kumbalgodu Ayyappa Temple Pooja Reminder',
                             body=f'{b.temple} - {b.pooja} pooja in your name will be conducted tomorrow')
        if b.devotee.phone:
            send_sms.delay(flow_id="606d7435642bde48ce7cbf83", number=f"91{b.devotee.phone}")
