from datetime import datetime

import pytz
import razorpay
from flask import Blueprint, request, current_app
from jsonschema.validators import validate
from werkzeug.exceptions import BadRequest

from app.api.schemas import *
from app.models import Devotee, Setting
from app.utils import APIViewMedia, APIView

admin = Blueprint('admin', __name__, url_prefix='/admin')

APIViewMedia.register(admin, 'post', '/post/', Post, PostSchema(), [])
APIView.register(admin, 'volunteer', '/volunteer/', Volunteer, VolunteerSchema(), [])


class PoojaAPIView(APIViewMedia):
    def before_parse_data(self, data):
        if data.get('amount'):
            data['amount'] = float(data['amount'])

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
            if self.schema.validation_schema['properties'][k].get('format') == 'utc-millisec':
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


BookingAPIView.register(admin, 'booking', '/booking/', Booking, BookingSchema(), [])

APIView.register(admin, 'settings', '/settings/', Setting, SettingSchema())

from .gallery import gallery

admin.register_blueprint(gallery)
