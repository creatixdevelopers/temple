import json
from datetime import datetime
from functools import wraps
from typing import Any

import pytz
from flask import request, jsonify, render_template, redirect, url_for
from flask.views import View, MethodView
from flask_jwt_extended import verify_jwt_in_request, get_current_user, get_jwt, unset_jwt_cookies
from flask_jwt_extended.exceptions import JWTExtendedException
from jwt.exceptions import PyJWTError
from jsonschema.validators import validate
from werkzeug.exceptions import NotFound, Unauthorized


def current_user():
    try:
        verify_jwt_in_request()
        return get_current_user()
    except Exception:
        return None


def role_required(roles: list[str], redirect_to='dashboard.login') -> Any:
    """Ensures that the current user is authorized to access the wrapped route. If the user is unauthorized, they are
    redirected to the login page.
    :param roles: list of roles that are authorized to access this route.
    :param redirect_to: path to redirect to if not logged in. JSON response is sent if not set.
    :return: Flask route, redirect or error."""

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                if get_jwt().get('subr') not in roles:
                    raise Unauthorized
            except (JWTExtendedException, PyJWTError) as e:
                response = redirect(url_for(redirect_to)) if redirect_to else \
                    (jsonify({'status': 'failure', 'code': 403, 'description': 'Forbidden'}), 403)
                unset_jwt_cookies(response[0] if isinstance(response, tuple) else response)
                return response
            except Exception as e:
                raise e
            return fn(*args, **kwargs)

        return decorator

    return wrapper


class APIView(MethodView):

    def __init__(self, model, schema):
        self.model = model
        self.schema = schema

    def parse_data(self, data) -> dict:
        data = {k: (data[k] if k in data else None) for k in self.schema.validation_schema['properties'].keys()}
        for k, v in data.items():
            if self.schema.validation_schema['properties'][k].get('format') == 'utc-millisec':
                data[k] = datetime.fromtimestamp(v / 1000, tz=pytz.timezone("Asia/Kolkata")).replace(tzinfo=None)
        return data

    def after_post(self, data, r):
        pass

    def after_put(self, data, r):
        pass

    def get(self, uid: str = None):
        if not uid:
            r = self.model.get_by(**request.args.to_dict()) if request.args else self.model.all()
            return jsonify({'status': 'success', 'code': 200, 'data': self.schema.dump(r, many=True)}), 200
        else:
            if r := self.model.get_by(first=True, uid=uid):
                return jsonify({'status': 'success', 'code': 200, 'data': self.schema.dump(r)}), 200
            raise NotFound

    def post(self):
        data = request.get_json()
        validate(data, self.schema.validation_schema)
        data = self.parse_data(data)
        r = self.model.create(**data)
        self.after_post(data, r)
        return jsonify({'status': 'success', 'code': 200, 'data': self.schema.dump(r)}), 200

    def put(self, uid: str):
        data = request.get_json()
        validate(data, self.schema.validation_schema)
        data = self.parse_data(data)
        if r := self.model.get_by(first=True, uid=uid):
            r.update(**data)
            self.after_put(data, r)
            return jsonify({'status': 'success', 'code': 200, 'data': self.schema.dump(r)}), 200
        raise NotFound

    def delete(self, uid: str):
        if 'deleted' in self.model.__dict__:
            if r := self.model.query.with_deleted().filter_by(uid=uid).first():
                if request.url_rule.rule.endswith('/restore/'):
                    r.update(deleted=False)
                else:
                    r.delete() if r.deleted else r.update(deleted=True)
                return jsonify({'status': 'success', 'code': 200}), 200
            raise NotFound
        else:
            if r := self.model.get_by(first=True, uid=uid):
                r.delete()
                return jsonify({'status': 'success', 'code': 200}), 200
            raise NotFound

    @classmethod
    def register(cls, bp, endpoint, url, model, schema, decorators=None, methods=None):
        decorators = [] if decorators is None else decorators
        methods = ['GET', 'POST', 'PUT', 'DELETE'] if methods is None else methods

        cls.decorators = decorators
        view_func = cls.as_view(endpoint, model=model, schema=schema)
        if methods is None:
            methods = ['GET', 'POST', 'PUT', 'DELETE']
        if 'GET' in methods:
            bp.add_url_rule(url, defaults={'uid': None}, view_func=view_func, methods=['GET'])
            bp.add_url_rule(f'{url}<string:uid>/', view_func=view_func, methods=['GET'])
        if 'POST' in methods:
            bp.add_url_rule(url, view_func=view_func, methods=['POST'])
        if 'PUT' in methods:
            bp.add_url_rule(f'{url}<string:uid>/', view_func=view_func, methods=['PUT'])
        if 'DELETE' in methods:
            bp.add_url_rule(f'{url}<string:uid>/', view_func=view_func, methods=['DELETE'])
            bp.add_url_rule(f'{url}<string:uid>/restore/', view_func=view_func, methods=['DELETE'])


class APIViewImages(APIView):

    def __init__(self, model, schema):
        super().__init__(model, schema)

    def post(self):
        data = request.form.to_dict()
        validate(data, self.schema.validation_schema)
        data = self.parse_data(data)
        r = self.model.create(**data)
        images = list(request.files.values())
        if r and images:
            r.save_images(images)
        self.after_post(data, r)
        return jsonify({'status': 'success', 'data': self.schema.dump(r)}), 200

    def put(self, uid: str):
        data = request.form.to_dict()
        validate(data, self.schema.validation_schema)
        data = self.parse_data(data)
        if r := self.model.get_by(first=True, uid=uid):
            r.update(**data)
            images = list(request.files.values())
            retained = json.loads(data['retained'])
            if r and images and isinstance(retained, list):
                r.delete_images(set(r.images) ^ set(retained))
                r.save_images(images)
            self.after_put(data, r)
            return jsonify({'status': 'success', 'data': self.schema.dump(r)}), 200
        raise NotFound


class RouteView(View):

    def __init__(self, template, template_kwargs):
        self.template = template
        self.template_kwargs = template_kwargs

    def dispatch_request(self, **kwargs):
        return render_template(self.template, **kwargs, **self.template_kwargs)

    @classmethod
    def register(cls, bp, endpoint, urls, template, template_kwargs=None, decorators=None, methods=None):
        template_kwargs = {} if template_kwargs is None else template_kwargs
        decorators = [] if decorators is None else decorators
        methods = ['GET'] if methods is None else methods

        cls.decorators = decorators
        view_func = cls.as_view(endpoint, template=template, template_kwargs=template_kwargs)
        urls = {urls: {}} if isinstance(urls, str) else urls
        for url, defaults in urls.items():
            bp.add_url_rule(url, defaults=defaults, view_func=view_func, methods=methods)
