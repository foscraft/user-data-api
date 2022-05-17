import os
from decouple import config

class Config:
    DEBUG=False
    TESTING=False
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG=True

class ProductionConfig(Config):
    ...

class TestingConfig(Config):
    TESTING=True