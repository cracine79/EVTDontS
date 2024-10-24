from decouple import config
import os
from os import getenv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config: 
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= config('DATABASE_URL')
    TESTING=False
    DEBUG=False
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = config('AWS_S3_BUCKET')
    AWS_REGION = config('AWS_REGION')


class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    DEVELOPMENT=True

class ProdConfig(Config):
    DEBUG=False

class TestConfig(Config):
    TESTING=True