from server.utilis.api_response import ApiResponse
from flask import Blueprint, request
from flask_jwt_extended import jwt_required ,get_jwt
from server.services.service_factory import get_auth_service

auth_bp = Blueprint("auth", __name__)

# Registers a user
@auth_bp.route("/sign_up", methods=["POST"])
def sign_up():
    # Get user input from request and parse it 
    user_input = request.get_json()

    if not user_input:
        return ApiResponse.error(
            message="No data provided",
            status_code=400
        )

    
    auth_service=get_auth_service()
    # Call auth service to register a user 
    result = auth_service.register_user(user_input)

    user = result["user"]

    return ApiResponse.success(
        data={
            "id": user.id,
            "email_address": user.email_address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "access_token": result["access_token"]
        },
        message="User registered successfully",
        status_code=201
    )

@auth_bp.route("/sign_in", methods=["POST"])
def sign_in():

    # Parse request JSON
    login_input = request.get_json()

    if not login_input:
        return ApiResponse.error(
            message="No data provided",
            status_code=400
        )

    auth_service=get_auth_service()
    # Call service
    result = auth_service.login_user(login_input)

    user = result["user"]

    return ApiResponse.success(
        data={
            "id": user.id,
            "email_address": user.email_address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "access_token": result["access_token"]
        },
        message="Login successful",
        status_code=200
    )

# send email verification link -protected route
@auth_bp.route("/send_verification_email", methods=["POST"])
@jwt_required()
def send_verification_email():
    #get jwt payload
    claims = get_jwt()
    #user_id is stored as string convert it to interger
    user_id = int(claims["sub"])

    auth_service = get_auth_service()

    auth_service.send_email_verification_link(user_id)

    return ApiResponse.success(
        message="Verification email sent"
    )