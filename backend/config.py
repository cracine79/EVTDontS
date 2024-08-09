from decouple import config
import os
from os import getenv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config: 
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= 'postgresql://postgres:1234@localhost:5432/evtds_db'
    TESTING=False
    DEBUG=False

class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    DEVELOPMENT=True

class ProdConfig(Config):
    DEBUG=False

class TestConfig(Config):
    TESTING=True