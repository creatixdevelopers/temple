from flask import Blueprint, jsonify
from jsonschema.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError

api = Blueprint('api', __name__, url_prefix='/api')


def error_handler(e):
    if not isinstance(e, HTTPException):
        if isinstance(e, ValidationError):
            e = BadRequest()
        elif isinstance(e, IntegrityError):
            return jsonify(
                {'status': 'error', 'code': 409, 'name': 'Integrity Error', 'description': 'An entry with those details already exists.'}), 409
        else:
            e = InternalServerError()
    return jsonify({'status': 'error', 'code': e.code, 'name': e.name, 'description': e.description}), e.code


api.error_handler = error_handler

from .auth import auth
from .admin import admin
from .public import public

api.register_blueprint(auth)
api.register_blueprint(admin)
api.register_blueprint(public)
