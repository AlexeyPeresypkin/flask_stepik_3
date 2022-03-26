import os

from dotenv import load_dotenv

load_dotenv()
current_path = os.path.dirname(os.path.realpath(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMAGE_UPLOADS = os.path.join(current_path, 'static', 'image_uploads')
    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMAGE_UPLOADS = os.path.join(current_path, 'static', 'image_uploads')
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = False
