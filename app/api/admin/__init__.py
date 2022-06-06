from datetime import datetime

import pytz
import razorpay
from flask import Blueprint, current_app, request
from jsonschema.validators import validate

from app.api.schemas import *
from app.utils import APIViewMedia, APIView

admin = Blueprint('admin', __name__, url_prefix='/admin')

APIViewMedia.register(admin, 'post', '/post/', Post, PostSchema(), [])
APIView.register(admin, 'volunteer', '/volunteer/', Volunteer, VolunteerSchema(), [])
APIView.register(admin, 'pooja', '/pooja/', Pooja, PoojaSchema(), [])
APIView.register(admin, 'donation', '/donation/', Donation, DonationSchema(), [])


class BookingAPIView(APIView):
    def parse_data(self, data) -> dict:
        data = {k: (data[k] if k in data else None) for k in self.schema.validation_schema['properties'].keys()}
        for k, v in data.items():
            if self.schema.validation_schema['properties'][k].get('format') == 'utc-millisec':
                data[k] = datetime.fromtimestamp(v / 1000, tz=pytz.timezone("Asia/Kolkata")).replace(tzinfo=None)
        pooja = Pooja.get(data['pooja_id'])
        if pooja:
            del data['pooja_id']
            data.update({'temple': pooja.temple, 'pooja': pooja.name, 'amount': pooja.amount})
        return data


BookingAPIView.register(admin, 'booking', '/booking/', Booking, BookingSchema(), [])

from .gallery import gallery

admin.register_blueprint(gallery)


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
    order = rz.order.create(data={'amount': data['amount']*100, 'currency': 'INR'})
    return {'status': 'success', 'data': {'order_id': order['id']}}, 200
