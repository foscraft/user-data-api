from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from app.models import User


@app.route("/api/v1/register", methods=["POST"])
def register():
  
    data = request.json

    hashed_password = generate_password_hash(
        data.get("password"), method="sha256"
    )

    user = User(
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        username=data.get("username"),
        bio=data.get("bio"),
        email=data.get("email"),
        password=hashed_password,
    )
    db.session.add(user)
    db.session.commit()
    return {
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "bio": user.bio,
            "email": user.email,
        }
    }, 201


@app.route("/api/v1/users", methods=["GET"])
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


@app.route("/api/v1/users/<id>", methods=["GET"])
def get_user_by_id(id):
    user = User.query.get(id)
    if not user:
        return abort(404)
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "username": user.username,
        "bio": user.bio,
    }
    return {"user": user_data}, 200


@app.route("/api/v1/login", methods=["POST"])
def login():
    data = request.json
    password = data.get("password")
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            session["logged_in"] = True
            session["email"] = user.email
            session["username"] = user.username
            return {"message": f"You are logged in as {user.username}"}, 200
        else:
            return {"message": "Username or Password Incorrect"}, 400
    return {"message": "user does not have an account"}, 404


@app.route("/api/v1/logout", methods=["GET"])
def logout():
    session.pop("logged_in", None)
    session.pop("email", None)
    session.pop("username", None)
    return {"message": "You are logged out"}, 200


@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = User.query.filter_by(id=user_id).first()

    if user:
        user.first_name = data.get("first_name")
        user.last_name = data.get("last_name")
        user.username = data.get("username")
        user.bio = data.get("bio")
        db.session.commit()
        return {"message": "User updated"}, 200
    return {"message": "User not found"}, 404
