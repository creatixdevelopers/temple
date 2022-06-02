import json
import os

from flask import Blueprint, current_app, request
from jsonschema.validators import validate

from app.services import save_file, delete_file

gallery = Blueprint('gallery', __name__, url_prefix='/gallery')


@gallery.get('/')
def get():
    try:
        path = os.path.join(current_app.config['UPLOADS_FOLDER'], 'gallery')
        return {'status': 'success', 'data': os.listdir(path)}, 200
    except Exception:
        return {'status': 'failure'}, 500


@gallery.put('/')
def put():
    data = request.form.to_dict()
    validate(data, {
        "type": "object",
        "properties": {
            "retained": {"type": "string"},
        },
        "required": ["retained"],
    })
    files = list(request.files.values())
    path = os.path.join(current_app.config['UPLOADS_FOLDER'], 'gallery')
    if not os.path.exists(path):
        os.makedirs(path)
    [delete_file(os.path.join(path, file)) for file in list(set(os.listdir(path)) ^ set(json.loads(data['retained'])))]
    [save_file(path, file) for file in files]
    return {'status': 'success'}, 200
