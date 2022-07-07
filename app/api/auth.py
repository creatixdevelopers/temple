from datetime import timedelta

from flask import Blueprint, request, make_response, url_for, jsonify, current_app
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, unset_jwt_cookies, get_jwt
from jsonschema.validators import validate

from app.models import User
from app.services import r
from app.tasks import send_email

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.post('/login/')
def login():
    data = request.get_json()
    validate(data, {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email", "pattern": "^\\S+@\\S+\\.\\S+$", "minLength": 5, "maxLength": 127},
            "password": {"type": "string", "minLength": 8, "maxLength": 30},
            "remember": {"type": "boolean"},
        },
        "required": ["email", "password", "remember"],
    })
    if (user := User.get_by(first=True, email=data['email'])) and user.verify_password(data['password']) and (role := user.role.name) in ['admin', 'user']:
        response = make_response(jsonify({'status': 'success', 'code': 200}), 200)
        access_token = create_access_token(identity=user.uid, additional_claims={'subr': role}, fresh=True)
        set_access_cookies(response, access_token, max_age=(timedelta(days=7) if data['remember'] else None))
        return response
    return jsonify({'status': 'error', 'code': 401, 'name': 'Unauthorized', 'description': 'Invalid Credentials'}), 401


@auth.post('/logout/')
@jwt_required()
def logout():
    claims = get_jwt()
    r.set(name=claims['jti'], value='', ex=(claims['exp'] - r.time()[0]))
    response = make_response(jsonify({'status': 'success', 'code': 200}), 200)
    unset_jwt_cookies(response)
    return response


@auth.post('/forgot-password/')
def forgot_password():
    data = request.get_json()
    validate(data, {
        "type": "object",
        "properties": {
            "email": {"type": "string", "format": "email", "pattern": "^\\S+@\\S+\\.\\S+$", "minLength": 5, "maxLength": 127},
        },
        "required": ["email"],
    })
    if (user := User.get_by(first=True, email=data['email'])) and user.role.name == 'user':
        reset_token = user.generate_reset_token()
        body = f'''Visit the following link to reset your password:\n{url_for('dashboard.reset_password', _external=True, token=reset_token)}\n\n
                            If you didn't request a change in your password, please contact support immediately.'''
        send_email.delay(subject=f"{current_app.config['APPLICATION_NAME']} - Reset Password", body=body, recipients=[user.email])
        return jsonify(
            {'status': 'success', 'code': 200,
             'description': "We've sent you an email with further instructions on how to reset your password."}), 200
    return jsonify({'status': 'failure', 'code': 400, 'description': 'Email not found in database!'}), 400


@auth.post("/reset-password/")
def reset_password():
    data = request.get_json()
    validate(data, {
        "type": "object",
        "properties": {
            "token": {"type": "string"},
            "password": {"type": "string", "minLength": 8, "maxLength": 30},
        },
        "required": ["password"],
    })
    if claims := User.verify_reset_token(data['token']):
        if (user := User.get_by(first=True, uid=claims.get('sub'))) and user.role.name == 'user':
            user.update(password=data['password'])
            r.set(name=claims['jti'], value='', ex=(claims['exp'] - r.time()[0]))
            return jsonify({'status': 'success', 'description': 'Password reset successfully!'}), 200
    return jsonify({'status': 'failure', 'code': 400, 'description': 'Invalid or expired token'}), 400
