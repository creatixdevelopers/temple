from flask import Blueprint

from app.api.schemas import *
from app.helpers import APIViewImages, role_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

APIViewImages.register(admin, 'post', '/post/', Post, PostSchema(), [])
