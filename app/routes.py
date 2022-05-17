from crypt import methods
import re
from app import app,db
from app.models import User
from flask import request, abort,jsonify,session
from werkzeug.security import  generate_password_hash,check_password_hash

@app.route('/register', methods =['POST'])
def register():
    data = request.json
    
    hashed_password = generate_password_hash(data.get("password"), method='sha256')
  
    user = User(
        first_name = data.get("first_name"),
        last_name =  data.get("last_name"),
        username =  data.get("username"),
        bio =  data.get("bio"),
        email =  data.get("email"),
        password = hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User created"}, 201

@app.route('/users', methods =['GET'])
def get_users():
    db_users = User.query.all()
    users = []
    for user in db_users:
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "bio": user.bio,                            
        }
        users.append(user_data)

    return {"users": users}, 200

@app.route('/users/<id>',methods=['GET'])
def get_user_by_id(id):
    user_details = User.query.filter_by(id=id)
    return {'details': user_details},200

@app.route('/login',methods=['POST'])
def login():
    data = request.json
    password = data.get("password")
    email = data.get("email")
    user = User.query.filter_by(email=email).first() 
    if user:
        if check_password_hash(user.password, password):
            session['logged_in'] = True
            session['email'] = user.email
            session['username'] = user.username
            return f'You are logged in as {user.username}',201
        else:
            return ('Username or Password Incorrect')
    return ('user does not have an account')

    