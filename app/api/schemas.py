from app.models import User
from app.services import ma


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = ['uid', 'created', 'email']

    validation_schema = {
        "type": "object",
        "properties": {
            "created": {"type": "number", "format": "utc-millisec"},
            "email": {"type": "string", "format": "email", "pattern": "^\\S+@\\S+\\.\\S+$", "minLength": 5, "maxLength": 128},
            "password": {"type": "string", "minLength": 8, "maxLength": 32},
        },
        "required": ["email", "password"],
    }
