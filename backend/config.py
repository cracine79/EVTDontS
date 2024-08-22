from decouple import config
import os
from os import getenv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config: 
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= config('DATABASE_URL')
    TESTING=False
    DEBUG=False
    JWT_BLACKLIST_ENABLED=True
    JWT_BLACKLIST_TOKEN_CHECKS=True

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    DEVELOPMENT=True

class ProdConfig(Config):
    DEBUG=False

class TestConfig(Config):
    TESTING=True