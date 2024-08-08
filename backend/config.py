from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config: 
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= os.environ['DATABASE_URL']
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