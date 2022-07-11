import json
from datetime import datetime

import pytz
import razorpay
from flask import Blueprint, request, current_app
from jsonschema.validators import validate
from werkzeug.exceptions import BadRequest

from app.api.schemas import *
from app.models import Devotee, Setting
from app.tasks import send_email, send_sms
from app.utils import APIViewMedia, APIView

admin = Blueprint('admin', __name__, url_prefix='/admin')

APIView.register(admin, 'volunteer', '/volunteer/', Volunteer, VolunteerSchema(), [])


class PostAPIView(APIViewMedia):
    def parse_data(self, data):
        if data.get('priority'):
            data['priority'] = int(data['priority'])
        return data


PostAPIView.register(admin, 'post', '/post/', Post, PostSchema(), [])


@admin.post('/header-events/')
def header_events():
    data = request.get_json()
    validate(data, {
        "type": "object",
        "properties": {
            "events": {"type": "array", "items": {"type": "integer"}},
        },
        "required": ["events"],
    })
    for event in Post.by_type('event'):
        event.update(priority=1)
    for i, event_id in enumerate(data['events']):
        Post.get(event_id).update(priority=(999-i))
    return {'status': 'success'}, 200


class PoojaAPIView(APIViewMedia):
    def before_parse_data(self, data):
        if data.get('amount'):
            data['amount'] = float(data['amount'])
        if data.get('specific'):
            data['specific'] = data['specific'] == 'true'
        if data.get('dates'):
            data['dates'] = json.loads(data['dates'])
        return data


PoojaAPIView.register(admin, 'pooja', '/pooja/', Pooja, PoojaSchema(), [])


@admin.post('/create-order/')
def create_order():
    data = request.get_json()
    validate(data, {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
        },
        "required": ["amount"],
    })
    rz = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY'], current_app.config['RAZORPAY_SECRET']))
    order = rz.order.create(data={'amount': data['amount'] * 100, 'currency': 'INR'})
    return {'status': 'success', 'data': {'order_id': order['id']}}, 200


class DonationAPIView(APIView):
    def parse_data(self, data) -> dict:
        data = {k: (data[k] if k in data else None) for k in self.schema.validation_schema['properties'].keys()}
        for k, v in data.items():
            if self.schema.validation_schema['properties'][k].get('format') == 'utc-millisec' and data[k]:
                data[k] = datetime.fromtimestamp(v / 1000, tz=pytz.timezone("Asia/Kolkata")).replace(tzinfo=None)
        rz = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY'], current_app.config['RAZORPAY_SECRET']))
        payment_details = data.pop('payment_details', None)
        if rz.utility.verify_payment_signature(payment_details):
            data['payment_id'] = payment_details['razorpay_payment_id']
            if d := Devotee.get_by(first=True, phone=data['phone']):
                d.update(name=data.pop('name', d.name), email=data.pop('email', d.email))
                del data['phone']
                data['devotee_id'] = d.id
            else:
                d = Devotee.create(name=data.pop('name'), phone=data.pop('phone'), email=data.pop('email', ''))
                data['devotee_id'] = d.id
            return data
        else:
            raise BadRequest

    def after_post(self, data, r):
        if r.devotee.email:
            send_email.delay(recipients=[r.devotee.email], subject='Kumbalgodu Ayyappa Temple Donation Receipt',
                             html=f'Thank you for donating. Click <a href="https://kumbalgoduayyappatemple.org/donation-receipt/{r.uid}">here</a> '
                                  f'to download receipt.')
        if r.devotee.phone:
            send_sms.delay(flow_id="606d7435642bde48ce7cbf83", number=f"91{r.devotee.phone}")


DonationAPIView.register(admin, 'donation', '/donation/', Donation, DonationSchema(), [])


class BookingAPIView(APIView):
    def parse_data(self, data) -> dict:
        data = {k: (data[k] if k in data else None) for k in self.schema.validation_schema['properties'].keys()}
        for k, v in data.items():
            if self.schema.validation_schema['properties'][k].get('format') == 'utc-millisec':
                data[k] = datetime.fromtimestamp(v / 1000, tz=pytz.timezone("Asia/Kolkata")).replace(tzinfo=None)
        rz = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY'], current_app.config['RAZORPAY_SECRET']))
        payment_details = data.pop('payment_details', None)
        if rz.utility.verify_payment_signature(payment_details):
            data['payment_id'] = payment_details['razorpay_payment_id']
            if pooja := Pooja.get(data.pop('pooja_id', 0)):
                data.update({'temple': pooja.temple, 'pooja': pooja.name, 'amount': pooja.amount})
            if d := Devotee.get_by(first=True, phone=data['phone']):
                d.update(name=data.pop('name', d.name), email=data.pop('email', d.email))
                del data['phone']
                data['devotee_id'] = d.id
            else:
                d = Devotee.create(name=data.pop('name'), phone=data.pop('phone'), email=data.pop('email', ''))
                data['devotee_id'] = d.id
            return data
        else:
            raise BadRequest

    def after_post(self, data, r):
        if r.devotee.email:
            send_email.delay(recipients=[r.devotee.email], subject='Kumbalgodu Ayyappa Temple Pooja Booking Receipt',
                             html=f'Thank you for booking the pooja. Click <a href="https://kumbalgoduayyappatemple.org/pooja-rec'
                                  f'eipt/{r.uid}">here</a> to download receipt.')
        if r.devotee.phone:
            send_sms.delay(flow_id="606d7435642bde48ce7cbf83", number=f"91{r.devotee.phone}")


BookingAPIView.register(admin, 'booking', '/booking/', Booking, BookingSchema(), [])

APIView.register(admin, 'settings', '/settings/', Setting, SettingSchema())

from .gallery import gallery

admin.register_blueprint(gallery)
