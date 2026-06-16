from flask import request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from app.blueprints.auth import auth_bp
from app.extensions import db
from app.models import User


@auth_bp.post("/register")
def register():
    # request.get_json() reads the JSON body sent by the frontend/client.
    data = request.get_json() or {}

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Basic validation: the API should clearly say what is missing.
    if not name or not email or not password:
        return {"error": "Name, email, and password are required."}, 400

    # Emails should be treated consistently, so we normalize them.
    email = email.lower().strip()

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return {"error": "A user with this email already exists."}, 409

    user = User(name=name.strip(), email=email)
    user.set_password(password)

    # Add the new user to the current database session.
    db.session.add(user)

    # Commit saves the user permanently to the database.
    db.session.commit() 

    return {
        "message": "Account created successfully.",
        "user": user.to_dict(),
    }, 201


@auth_bp.post("/login")
def login():
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "Email and password are required."}, 400

    email = email.lower().strip()

    user = User.query.filter_by(email=email).first()

    # Keep this message general so attackers cannot easily guess valid emails.
    if not user or not user.check_password(password):
        return {"error": "Invalid email or password."}, 401

    # JWT identity is the value we can later recover from protected routes.
    access_token = create_access_token(identity=str(user.id))

    return {
        "message": "Login successful.",
        "access_token": access_token,
        "user": user.to_dict(),
    }

@auth_bp.get("/me")
@jwt_required()
def get_current_user():
    # get_jwt_identity() gives us the identity we stored when creating the token.
    # In login(), we used str(user.id), so here we receive the user's ID.
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return {"error": "User not found."}, 404

    return {
        "user": user.to_dict()
    }
