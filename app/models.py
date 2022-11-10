# sourcery skip: avoid-builtin-shadow
from app import db


class User(db.Model):
    '''
    Model collecting user information
    '''
    __tablename__ = "users_table"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    bio = db.Column(db.String(200))
    email = db.Column(db.String(35), unique=True)
    password = db.Column(db.String(256))
