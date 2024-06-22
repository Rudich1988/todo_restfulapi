import os

from dotenv import load_dotenv


load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_SECRET_KEY = os.getenv('WTF_CSRF_SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", default="very-important")

    MAIL_DEFAULT_SENDER = "noreply@flask.com"
    MAIL_SERVER = "smtp.yandex.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
