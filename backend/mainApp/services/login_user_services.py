from flask import Flask, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    create_access_token,
    verify_jwt_in_request,
)
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db
from datetime import timedelta
from models.user_model import Users

def login_user_services(data):
    try:
        if not data:
            return "missing data"
        email = data.email
        password = data.password
        
        existing_user = Users.query.filter_by(email=email).first()
        if not existing_user:
            return "user not exist"
        identity = {
            "email": existing_user.email,
            "username": existing_user.username,
            "provider": existing_user.provider,
            "user_id": existing_user.id,
        }

        access_token = None
        try:
            access_token = create_access_token(
                identity=identity, expires_delta=timedelta(days=150)
            )
        except Exception as e:
            print(f"token is expired {str(e)}")
        if not access_token:
            return "failled to get access token"

        if existing_user and check_password_hash(existing_user.password,password):
            return {
                "email": existing_user.email,
                "username": existing_user.username,
                "provider": existing_user.provider,
                "user_id": existing_user.id,
                "access_token": access_token
            }

        elif existing_user and not check_password_hash(existing_user.password,password):
            return "password incorrect"

    except Exception as e:
        print(f"Error at login_user_services {str(e)}")
