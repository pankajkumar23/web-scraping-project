from flask import Flask,jsonify
from flask_jwt_extended import get_jwt_identity,create_access_token,verify_jwt_in_request
from werkzeug.security import generate_password_hash,check_password_hash
from database.db import db
from datetime import timedelta


from models.user_model import Users
def sign_up_user_services(data):
    try:
        if not data:
            return "missing data"
        username=data.username
        email=data.email
        password=data.password
        hashed_password=generate_password_hash(password)
        existing_user= Users.query.filter_by(email=email).first()
        if existing_user:
            return "users already existing!!"
        add_user=Users(username=username,email=email,password=hashed_password,provider="email")
        db.session.add(add_user)
        db.session.commit()
        identity ={
            "email":add_user.email,
            "username": add_user.username,
            "provider":add_user.provider,
            "user_id":add_user.id,

        }
        access_token=None
        try:
            access_token = create_access_token(
            identity=identity, expires_delta=timedelta(days=150))
        except Exception as e:
            return "token is expired"

        if not access_token :
            return "failled to get access token "

        return {"message":"user successfully added!!",
                        "username":add_user.username,
                        "email":add_user.email,
                        "id":add_user.id,
                        "access_token":access_token}
    except Exception as e:
        print(f"Error at sign_up_user_services {str(e)}")