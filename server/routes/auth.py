from server.utilis.api_response import ApiResponse
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from server.services.service_factory import get_auth_service

auth_bp = Blueprint("auth", __name__)

#User Registration
@auth_bp.route("/sign_up", methods=["POST"])
def sign_up():
    user_input = request.get_json()
    if not user_input:
        return ApiResponse.error(message="No data provided", status_code=400)

    result = get_auth_service().register_user(user_input)
    user = result["user"]

    return ApiResponse.success(
        data={
            "id": user.id,
            "email_address": user.email_address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "access_token": result["access_token"],
            "email_sent": result["verification_email_sent"],
        },
        message="User registered successfully",
        status_code=201,
    )

#Handles user Login
@auth_bp.route("/sign_in", methods=["POST"])
def sign_in():
    login_input = request.get_json()
    if not login_input:
        return ApiResponse.error(message="No data provided", status_code=400)

    result = get_auth_service().login_user(login_input)
    user = result["user"]

    return ApiResponse.success(
        data={
            "id": user.id,
            "email_address": user.email_address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "access_token": result["access_token"],
        },
        message="Login successful",
        status_code=200,
    )

#Improvements -add api rate limiting
@auth_bp.route("/send_verification_email", methods=["POST"])
@jwt_required()
def send_verification_email():
    user_id = int(get_jwt()["sub"])
    email_sent=get_auth_service().resend_verification_email(user_id)
    return ApiResponse.success(
        data={"email_sent": email_sent},
        message="If the email is valid, a verification link has been sent.",
    )


@auth_bp.route("/verify_email", methods=["GET"])
def verify_email():
    token = request.args.get("token")
    if not token:
        return ApiResponse.error(message="Verification token required", status_code=400)

    get_auth_service().verify_email(token)
    return ApiResponse.success(message="Email verified successfully")
