import traceback

from celery.utils.log import get_task_logger

from app.services import celery

logger = get_task_logger(__name__)
import requests


@celery.task
def send_sms(flow_id, number):
    return True
    try:
        payload = {
            "flow_id": flow_id,
            "sender": "DFRDLY",
            "mobiles": number,
            "DF_BRAND_FRIEND_NAME": "Kumbalgodu",
            "DF_BUSINESS_NAME": "Ayyappa",
            "DF_FRIENDLY_CODE": "123",
            "DF_BUSINESS_PHONE": "9999999999",
            "DF_BUSINESS_MAP_LINK": "3",
            "DF_BUSINESS_WEBSITE_LINK": "1"
        }
        headers = {
            "authkey": "220891AfpFUypD5b2dab3a",
            "content-type": "application/JSON"
        }
        response = requests.post("https://api.msg91.com/api/v5/flow/", json=payload, headers=headers)
        print(response.status_code, response.json())
        return True
    except Exception as e:
        logger.critical(f"{str(e)} \n {traceback.format_exc()}\n\n")
        return False
