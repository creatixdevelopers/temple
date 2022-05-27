from flask import Blueprint

from app.api.schemas import *
from app.helpers import APIView, role_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

APIView.register(admin, 'user', '/user/', User, UserSchema(), [role_required(['admin'], False)])
