from decouple import config


class Config:
    '''Base config class'''
    DEBUG = False
    TESTING = False
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    '''Development config class'''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")


class ProductionConfig(Config):
    '''Production config class'''
    ...


class TestingConfig(Config):
    '''Testing config class'''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"
