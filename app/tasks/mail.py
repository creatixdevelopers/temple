import traceback

from celery.utils.log import get_task_logger
from flask_mail import Message

from app.services import mail, celery
from config import BaseConfig

logger = get_task_logger(__name__)


@celery.task
def send_error_email(e, tb):
    try:
        message = Message(f"Error in {BaseConfig.APPLICATION_NAME}", recipients=BaseConfig.ADMIN_EMAILS)
        message.body = f'Error: {str(e)} \n\n Traceback: {tb}'
        mail.send(message)
        return True
    except Exception as e:
        logger.critical(f"{str(e)} \n {traceback.format_exc()}\n\n")
        return False


@celery.task
def send_email(recipients, subject, body='', html='', attachments=None):
    attachments = {} if attachments is None else attachments
    try:
        message = Message(subject=subject, recipients=recipients)
        message.body = body
        message.html = html
        for file, mime in attachments.items():
            with open(file, 'rb') as f:
                message.attach(file, mime, f.read())
        mail.send(message)
        return True
    except Exception as e:
        logger.critical(f"{str(e)} \n {traceback.format_exc()}\n\n")
        send_error_email.delay(str(e), traceback.format_exc())
        return False
