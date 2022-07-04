import hashlib
import hmac
import importlib
import inspect
import json
import logging
import math
import traceback
import urllib
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

import pytz
from flask import Flask, send_from_directory, make_response, request, render_template_string as rts
from flask.logging import default_handler
from werkzeug.exceptions import HTTPException

from app.services import talisman, csrf, db, migrate, jwt, socketio, ma, mail, celery, r, india_time
from app.tasks import send_error_email
from app.utils import current_user


def create_app(config: str = 'config.DevelopmentConfig') -> Flask:
    """Creates, initializes and returns the flask application object using the past configuration
    :param config: Relative path to the configuration class to be used
    :return: Flask application object
    """

    app = Flask(__name__)
    app.config.from_object(config)

    # Initializing services
    for service in [csrf, db, jwt, ma, mail]:
        service.init_app(app)
    socketio.init_app(app)
    migrate.init_app(app, db)
    init_celery(app)

    # Initializing CLI commands
    from app.commands import dev_commands, test_command
    if app.config['TESTING']:
        app.cli.add_command(dev_commands)
    app.cli.add_command(test_command)

    # Importing and registering blueprints
    from app.api import api
    from app.dashboard import dashboard
    from app.site import site

    blueprints = [api, dashboard, site]
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    @app.post('/cd/')
    @csrf.exempt
    def cd():
        sig = f"sha256={hmac.new(bytes(app.config['SECRET_KEY'], 'utf-8'), msg=request.data, digestmod=hashlib.sha256).hexdigest()}"
        if hmac.compare_digest(sig.lower(), request.headers.get('X-Hub-Signature-256', '')):
            if request.get_json().get('ref').split('/')[-1] == 'production':
                from app.tasks import continuous_development
                continuous_development.delay()
                return {'status': 'success'}, 200
            return {'status': 'ignored'}, 400
        return {'status': 'failure'}, 400

    # Configuring logging
    my_handler = RotatingFileHandler(app.config['LOG_FILE'], maxBytes=10485760, backupCount=5)
    my_handler.setLevel(logging.INFO)
    my_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s[in %(filename)s: %(lineno)d]\n' + f'{"-" * 100}\n'))

    app.logger.handlers.clear()
    app.logger.removeHandler(default_handler)
    app.logger.handlers.extend(logging.getLogger('gunicorn.error').handlers)
    app.logger.handlers.append(my_handler)

    init_global_funcs(app, blueprints)

    return app


def init_global_funcs(app: Flask, blueprints: list):
    @app.errorhandler(Exception)
    def error(e):
        app.logger.critical(f'{str(e)}\n{traceback.format_exc()}\n')
        if not isinstance(e, HTTPException):
            send_error_email.delay(str(e), traceback.format_exc())
        for blueprint in blueprints:
            if request.path.startswith(f'{blueprint.url_prefix}/'):
                return blueprint.error_handler(e)
        return "Page not found.", 404

    @app.context_processor
    def context_processor():
        models = {}
        for _, cls in inspect.getmembers(importlib.import_module('app.models'), inspect.isclass):
            if issubclass(cls, db.Model):
                models[cls.__name__] = cls
        return {**models, 'rts': rts, 'current_user': current_user, 'r': r, 'india_time': india_time, 'datetime': datetime, 'timedelta': timedelta,
                'pytz': pytz}

    # Configure PWA if enabled
    if app.config['PWA']:
        def manifest():
            return send_from_directory(directory='static', path='pwa/manifest.json')

        def sw():
            response = make_response(send_from_directory(directory='static', path='pwa/sw.js'))
            response.headers['Cache-Control'] = 'no-cache'
            return response

        app.add_url_rule('/manifest.json', view_func=manifest)
        app.add_url_rule('/sw.js', view_func=sw)

    # Jinja template filters
    @app.template_filter('json_loads')
    def json_loads(s):
        return json.loads(s)

    @app.template_filter('inr_format')
    def inr_format(n):
        s, *d = str(n).partition(".")
        r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
        return "".join([r] + d)

    @app.template_filter('url_encode')
    def inr_format(s):
        return urllib.parse.quote_plus(s) if s else ''

    @app.template_filter('index_by_attributes')
    def index_by_attributes(d, **kwargs):
        return [i for i, (k, v) in enumerate(d.items()) if all([v.get(k1, False) == v1 for k1, v1 in kwargs.items()])]

    @app.template_filter('sum_of_product_of_attributes')
    def sum_of_product_of_attributes(l, a):
        return sum([math.prod([i.get(a1) for a1 in a]) for i in l])


def init_celery(app: Flask = None):
    app = app or create_app()
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
