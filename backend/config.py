from decouple import config
import os
from os import getenv

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config: 
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI= config('DATABASE_URL').replace("postgres://", "postgresql://")
    TESTING=False
    DEBUG=False
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = config('AWS_S3_BUCKET')
    AWS_REGION = config('AWS_REGION')
    APP_DOMAIN = config('APP_DOMAIN', default='http://localhost:5173')
    # Public canonical domain used in SEO tags, sitemap.xml and robots.txt
    SITE_URL = config('SITE_URL', default='https://www.economicsvideos.com').rstrip('/')


class DevConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    DEVELOPMENT=True
    APP_DOMAIN = config('DEV_APP_DOMAIN', default='http://localhost:5173')
    ENV = 'development'
    
class ProdConfig(Config):
    DEBUG=True
    APP_DOMAIN = config('PROD_APP_DOMAIN', default='https://www.evtds.com')
    ENV = 'production'

class TestConfig(Config):
    TESTING=True
    APP_DOMAIN = config('TEST_APP_DOMAIN', default='http://localhost:5173')
    ENV = 'testing'
