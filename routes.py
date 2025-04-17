from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
# from app import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token

user_routes = Blueprint("user_routes", __name__)

def get_db():
    from app import db
    return db

def get_bcrypt():
    from app import bcrypt
    return bcrypt

@user_routes.route("/user", methods=["GET"])
def get_user():
    db = get_db()
    users = db.session.execute(db.select(User).order_by(User.id)).scalars().all()
    if not users:
        return jsonify({"message": "No users found"}), 404
    
    return jsonify([{"id": user.id, "nama": user.nama, "username": user.username, "password": user.password, "email": user.email,} for user in users])

@user_routes.route("/user/register", methods=["POST"])
def register():
    db = get_db()
    bcrypt = get_bcrypt()
    
    data = request.json
    hashed_password = bcrypt.generate_password_hash(password=data["password"]).decode("utf-8")
    
    new_user = User(
        username=data["username"],
        password=hashed_password,
        email=data["email"],
        nama=data["nama"],
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered"}), 201
    except SQLAlchemyError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    
@user_routes.route("/user/login", methods=["POST"])
def login():
    db = get_db()
    bcrypt = get_bcrypt()
    
    data = request.json
    user = db.session.execute(db.select(User).where(User.username == data["username"])).scalar_one_or_none()
    
    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = create_access_token(identity=user.id)
    return jsonify({
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "nama": user.nama,
        }
    }), 200
    
@user_routes.route("/user/<int:id>", methods=["PUT"])
def update_user(id):
    db = get_db()
    bcrypt = get_bcrypt()
    
    data = request.json
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    if "password" in data and data["password"]:
        user.password = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
    
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.nama = data.get("nama", user.nama)
    
    db.session.commit()
    return jsonify({"message": "User updated successfully"}), 200

@user_routes.route("/user/<int:id>", methods=["DELETE"])
def delete_user(id):
    db = get_db()
    
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200