from app.models import Post, Volunteer, Donation, Pooja, Booking, Setting
from app.services import ma


class SettingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Setting

    validation_schema = {
        "type": "object",
        "properties": {
            "value": {"type": "string"},
        },
        "required": ["value"],
    }


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

    validation_schema = {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": ['blog', 'event']},
            "title": {"type": "string", "maxlength": 40},
            "description": {"type": "string", "maxLength": 250},
            "content": {"type": "string"},
            "retained": {"type": "string"},
        },
        "required": ["type", "title", "description", "content", "retained"],
    }


class VolunteerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Volunteer

    validation_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "maxlength": 128},
            "phone": {"type": "string", "maxlength": 10},
            "occupation": {"type": "string", "maxlength": 64},
            "email": {"type": "string", "format": "email", "maxlength": 128},
            "identification": {"type": "string", "maxlength": 14},
            "age": {"type": "integer", "min": 0, "max": 99},
            "address": {"type": "string", "maxlength": 512},
            "city": {"type": "string", "maxlength": 64},
            "pincode": {"type": "integer"},
            "comments": {"type": "string", "maxlength": 512},
        },
        "required": ["name", "phone", "occupation"],
    }


class DonationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Donation

    validation_schema = {
        "type": "object",
        "properties": {
            "amount": {"type": "number"},
            "type": {"type": "string",
                     "enum": ["Nitya Seva (Daily cow feed, oil & flower)", "Ghoshala Fund", "Annadaana Fund", "Building Fund", "Life Membership",
                              "General Donation"]},
            "name": {"type": "string", "maxlength": 128},
            "phone": {"type": "string", "maxlength": 10},
            "email": {"type": "string", "format": "email", "maxlength": 128},
            "aadhaar": {"type": "string", "minlength": 12, "maxlength": 12},
            "pan": {"type": "string", "minlength": 10, "maxlength": 10},
            "recurring_interval": {"type": "string", "enum": ["monthly", "yearly"]},
            "number": {"type": "integer"},
            "start_date": {"type": "integer", "format": "utc-millisec"},
            "payment_details": {
                "type": "object",
                "properties": {
                    "razorpay_payment_id": {"type": "string"},
                    "razorpay_order_id": {"type": "string"},
                    "razorpay_signature": {"type": "string"},
                },
                "required": ["razorpay_payment_id", "razorpay_order_id", "razorpay_signature"],
            }
        },
        "required": ["amount", "type", "name", "phone", "payment_details"]
    }


class PoojaSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Pooja

    validation_schema = {
        "type": "object",
        "properties": {
            "temple": {"type": "string", "maxlength": 128},
            "name": {"type": "string", "maxlength": 128},
            "amount": {"type": "number"},
            "specific": {"type": "boolean"},
            "dates": {"type": "array", "items": {"type": "number", "format": "utc-millisec"}},
            "description": {"type": "string"},
            "link": {"type": "string"},
        },
        "anyOf": [
            {"required": ["temple", "name", "amount", "specific"]},
            {"required": ["description"]},
        ]
    }


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking

    validation_schema = {
        "type": "object",
        "properties": {
            "pooja_id": {"type": "integer"},
            "name": {"type": "string", "maxlength": 128},
            "phone": {"type": "string", "maxlength": 10},
            "email": {"type": "string", "format": "email", "maxlength": 128},
            "gotra": {"type": "string", "maxlength": 128},
            "nakshatra": {"type": "string", "maxlength": 128},
            "days": {"type": "array", "items": {"type": "integer", "format": "utc-millisec"}},
            "booked_by_id": {"type": "integer"},
            "payment_details": {
                "type": "object",
                "properties": {
                    "razorpay_payment_id": {"type": "string"},
                    "razorpay_order_id": {"type": "string"},
                    "razorpay_signature": {"type": "string"},
                },
                "required": ["razorpay_payment_id", "razorpay_order_id", "razorpay_signature"],
            },
        },
        "required": ["pooja_id", "name", "phone", "days", "payment_details"],
    }
