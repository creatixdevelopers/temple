from app.models import Post, Volunteer, Donation, Pooja, Booking
from app.services import ma


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post

    validation_schema = {
        "type": "object",
        "properties": {
            "type": {"type": "string", "enum": ['blog', 'event']},
            "title": {"type": "string", "maxlength": 40},
            "content": {"type": "string"},
            "retained": {"type": "string"},
        },
        "required": ["type", "title", "content", "retained"],
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
            "name": {"type": "string", "maxlength": 128},
            "phone": {"type": "string", "maxlength": 10},
            "email": {"type": "string", "format": "email", "maxlength": 128},
            "identification": {"type": "string", "maxlength": 14},
            "type": {"type": "string", "enum": ["Nitya Seva", "Ghoshala Fund", "Annadaana Fund", "Building Fund"]},
            "amount": {"type": "number"},
            "recurring": {"type": "boolean"},
            "recurring_interval": {"type": "string", "enum": ["one-time", "monthly"]},
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
        "required": ["name", "phone", "identification", "type", "amount", "recurring", "recurring_interval", "payment_details"],
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
        },
        "required": ["temple", "name", "amount"],
    }


class BookingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Booking

    validation_schema = {
        "type": "object",
        "properties": {
            "pooja_id": {"type": "integer"},
            "name": {"type": "string", "maxlength": 128},
            "phone": {"type": "string", "maxlength": 14},
            "email": {"type": "string", "format": "email", "maxlength": 128},
            "gotra": {"type": "string", "maxlength": 128},
            "nakshatra": {"type": "string", "maxlength": 128},
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
        "required": ["pooja_id", "name", "phone", "payment_details"],
    }
