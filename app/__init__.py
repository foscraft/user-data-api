from decouple import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

env = config("ENV", "development")

if env == "development":
    app.config.from_object("config.DevelopmentConfig")

elif env == "production":
    app.config.from_object("config.ProductionConfig")

db = SQLAlchemy(app)

from app import routes

db.create_all()