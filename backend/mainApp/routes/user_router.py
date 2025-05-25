from flask import Flask,Blueprint,request,jsonify
from services.sign_up_user_services import sign_up_user_services
from schema.user_schema import SighinUserValidations,LoginUserValidations
from services.login_user_services import login_user_services
from services.get_hotel_data_services import get_hotel_data_services


user_router = Blueprint("users", __name__)

@user_router.route("/signup",methods=["POST"])
def sign_up_user():
    try:
        data = SighinUserValidations(**request.json)
        result = sign_up_user_services(data)
        if isinstance(result,str):
            return {"message":result},400
        return jsonify({"message":result}),200
    except Exception as e:
        print(f"error at sign_up_user {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500 


@user_router.route("/login",methods=["POST"])
def login_user():
    try:
        data = LoginUserValidations(**request.json)
        result = login_user_services(data)
        if isinstance(result,str):
            return {"message":result},400
        
        elif isinstance(result,dict):
            return {"message":result},200
        return jsonify({"message":result}),200
    
    except Exception as e:
        print(f"error at login_user {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500 
    




@user_router.route("/get-hotel-details",methods=["GET"])
def get_hotel_details():
    try:
        page = request.args.get("page",type=int)
        result = get_hotel_data_services(page)
        if isinstance(result,str):
            return {"message":result},400
        elif isinstance(result,dict):
            return {"message":result},200
        return jsonify({"message":result}),200
    
    except Exception as e:
        print(f"error at get_hotel_details {str(e)}")
        return jsonify({"message": "Internal Server Error", "error": str(e)}), 500 