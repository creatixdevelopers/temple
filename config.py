"""Contains configuration classes that set the application configuration settings at run-time."""
from os.path import join
from datetime import timedelta


class BaseConfig:
    APPLICATION_NAME = 'kumbalgodu_ayyappa'

    PWA = True
    WEB_SOCKETS = False
    UPLOADS_FOLDER = join('app', 'static', 'uploads')

    TESTING = True

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 604800

    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_ACCESS_COOKIE_NAME = 'access_token'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_SESSION_COOKIE = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = 'testingcreatix@gmail.com'
    MAIL_PASSWORD = 'bthowzkhnhjycjpj'
    MAIL_DEFAULT_SENDER = 'testingcreatix@gmail.com'
    MAIL_MAX_EMAILS = 1
    MAIL_ASCII_ATTACHMENTS = False
    MAIL_SUPPRESS_SEND = True
    ADMIN_EMAILS = ['creatixdevelopers@gmail.com']
    BACKUP_EMAILS = ['creatixdevelopers@gmail.com']

    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    result_backend = "redis://127.0.0.1:6379/0"

    LOG_FILE = './logs/app.log'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RAZORPAY_KEY = 'rzp_test_Gct2tFPysNEBMD'
    RAZORPAY_SECRET = 'AO2cLYxxI79sAYw8T69DwnJ9'


class TestConfig(BaseConfig):
    SECRET_KEY = '76fbece69658be45b890bc322a9dd83c08e75900aa1179'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../tests/test.db'
    LOG_FILE = './logs/test.log'


class DevelopmentConfig(BaseConfig):
    SECRET_KEY = '0a02b7bb087c3a36d59bb76488beac3f6fcbadd18cd565'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


class ProductionConfig(BaseConfig):
    TESTING = False
    SECRET_KEY = '6d638cbd006a11e68db153ac65488522bcfb13d52b7286'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///temple'
    MAIL_SUPPRESS_SEND = False
