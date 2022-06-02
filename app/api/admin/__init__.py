from datetime import datetime

import pytz
from flask import Blueprint

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
