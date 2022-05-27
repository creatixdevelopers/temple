import json
import os
import secrets
import uuid
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Union

import jwt as pyjwt
import pytz
from celery import Celery
from flask import current_app
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_talisman import Talisman
from flask_wtf import CSRFProtect
from redis import StrictRedis
from sqlalchemy import inspect, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_json import NestedMutableJson as Json
from werkzeug.security import generate_password_hash, check_password_hash

from config import BaseConfig

talisman = Talisman()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
socketio = SocketIO()
ma = Marshmallow()
mail = Mail()
celery = Celery(__name__, broker=BaseConfig.CELERY_BROKER_URL, backend=BaseConfig.result_backend)
r = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


# ------------------------- Helpers -------------------------

def random_uid(n: int = 7):
    return secrets.token_urlsafe(n)


def india_time() -> datetime:
    return datetime.now(pytz.timezone("Asia/Kolkata")).replace(tzinfo=None)


class ModelMixin(object):
    query: db.Query
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Text, default=random_uid, unique=True, index=True)

    @classmethod
    def columns(cls) -> dict:
        return {c.name: c.type for c in inspect(cls).columns}

    @classmethod
    def hybrid_properties(cls) -> list:
        return [i.__name__ for i in inspect(cls).all_orm_descriptors if type(i) == hybrid_property]

    @classmethod
    def commit(cls):
        db.session.commit()

    @classmethod
    def create(cls, commit=True, **kwargs):
        r = cls(**kwargs)
        db.session.add(r)
        if commit:
            cls.commit()
        return r

    @classmethod
    def get(cls, pk):
        return cls.query.get(pk)

    @classmethod
    def get_by(cls, first=False, **kwargs):
        q = cls.query.filter_by(**kwargs).order_by(cls.id)
        return q.first() if first else q.all()

    @classmethod
    def filter(cls, filters, first=False):
        q = cls.query.filter(*filters).order_by(cls.id)
        return q.first() if first else q.all()

    @classmethod
    def all(cls):
        return cls.query.order_by(cls.id).all()

    @classmethod
    def first(cls):
        return cls.query.order_by(cls.id).first()

    def update(self, commit=True, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        if commit:
            self.commit()

    def delete(self, commit=True):
        db.session.delete(self)
        if commit:
            self.commit()

    @classmethod
    def clear(cls, commit=False):
        cls.query.delete()
        if commit:
            cls.commit()

    def as_dict(self, include_hybrid_properties=False):
        r = {k: (getattr(self, k).timestamp() if isinstance(v, db.DateTime) else getattr(self, k)) for k, v in self.columns().items()}
        if include_hybrid_properties:
            for h in self.hybrid_properties():
                r[h] = getattr(self, h)
        return r

    def as_json(self, include_hybrid_properties=False):
        return json.dumps(self.as_dict(include_hybrid_properties), default=str)


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(self._only_full_mapper_zero('get'), session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None


class DeletedMixin(object):
    query_class = QueryWithSoftDelete
    deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def all_deleted(cls):
        return cls.query.with_deleted().filter_by(deleted=True).all()


class CreatedMixin(object):
    created = db.Column(db.DateTime, default=india_time)

    @classmethod
    def by_created_date(cls, start, end=None):
        start, end = tuple(x.date() if isinstance(x, datetime) else x for x in [start, end])
        if start and end:
            return cls.query.filter(cls.created.between(start, end)).all()
        else:
            return cls.query.filter(func.date(cls.created) == start).all()


class LastUpdatedMixin(object):
    last_updated = db.Column(db.DateTime, default=india_time, onupdate=india_time)


class ImagesMixin(object):
    images = db.Column(Json, default=[])

    UPLOADS_PATH = None

    def save_image(self, image):
        _, extension = os.path.splitext(image.filename)
        if extension in ['.jpg', '.jpeg', '.png']:
            filename = f'{random_uid(10)}{extension}'
            dir_path = os.path.join(current_app.config['UPLOADS_FOLDER'], self.UPLOADS_PATH if self.UPLOADS_PATH else '')
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            image.save(os.path.join(dir_path, filename))

            images = deepcopy(self.images)
            images.append(filename)
            self.update(images=images)
            return True
        return False

    def save_images(self, images):
        return [self.save_image(image) for image in images]

    def delete_image(self, name):
        if name in self.images:
            path = os.path.join(current_app.config['UPLOADS_FOLDER'], self.UPLOADS_PATH if self.UPLOADS_PATH else '', name)
            if os.path.exists(path):
                os.remove(path)

            images = deepcopy(self.images)
            images.remove(name)
            self.update(images=images)
            return True
        return False

    def delete_images(self, names):
        return [self.delete_image(name) for name in names]


class PasswordMixin(object):
    password_hash = db.Column(db.Text, nullable=False)

    @property
    def password(self) -> Exception:
        """Plain text password is not readable."""
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password: str) -> None:
        """Encrypts the passed password and sets it for the current user.
        :param password: The password to be set.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verifies the passed password matches the set password.
        :param password: The password to be verified.
        :return: `True` if passwords match otherwise `False`
        """
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self):
        return pyjwt.encode({'exp': datetime.utcnow() + timedelta(minutes=15), 'sub': self.uid, 'jti': str(uuid.uuid4())},
                            current_app.config['SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def verify_reset_token(token: str) -> Union[None, dict]:
        try:
            claims = pyjwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            return claims if (r.get(claims.get('jti')) is None) else None
        except Exception:
            return None
