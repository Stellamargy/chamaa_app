from server.utilis.api_response import ApiResponse
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from server.services.service_factory import get_auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# User Registration
@auth_bp.route("/sign_up", methods=["POST"])
def sign_up():
    # Get user registration data from request
    registration_input = request.get_json()
    if not registration_input:
        return ApiResponse.error(
            message="User registration data is required", status_code=400
        )

    registration_result = get_auth_service().register_user(registration_input)
    user = registration_result["user"]

    return ApiResponse.success(
        data={
            "id": user.id,
            "email_address": user.email_address,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "access_token": registration_result["access_token"],
            "email_sent": registration_result["verification_email_sent"],
        },
        message="User registered successfully",
        status_code=201,
    )


# Handles user Login
@auth_bp.route("/sign_in", methods=["POST"])
def sign_in():
    login_input = request.get_json()
    if not login_input:
        return ApiResponse.error(message="Login data is required", status_code=400)

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


# Improvements -add api rate limiting
@auth_bp.route("/send_verification_email", methods=["POST"])
@jwt_required()
def send_verification_email():
    user_id = int(get_jwt()["sub"])
    email_sent = get_auth_service().resend_verification_email(user_id)

    return ApiResponse.success(
        data={"email_sent": email_sent},
        message="Verification email sent.Check email inbox for verification link",
    )


@auth_bp.route("/verify_email", methods=["GET"])
def verify_email():
    token = request.args.get("token")
    if not token:
        return ApiResponse.error(
            message="This verification link is invalid. Please request a new one.",
            status_code=400,
        )
    # This has to return an access token because email is being verified .(STALE ACCESS TOKEN)
    verify_results = get_auth_service().verify_email(token)
    return ApiResponse.success(
        message="Your email has been verified successfully.",
        data={
            "user_id": verify_results["user"].id,
            "access_token": verify_results["access_token"],
        },
    )
