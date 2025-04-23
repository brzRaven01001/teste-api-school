import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    HOST = '0.0.0.0'
    PORT = 8000
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False