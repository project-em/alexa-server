import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    ROOT_URL = 'https://alexa.sachabest.com'
    DEBUG = True
    THREADED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False