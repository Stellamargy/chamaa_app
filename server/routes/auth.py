from server.utilis.api_response import ApiResponse
from flask import Blueprint, request
from marshmallow import ValidationError
from server.exceptions import ConflictError,AuthenticationError
from server.models import db
from server.repositories.user_repository import UserRepository
from server.services.auth_service import AuthService
import traceback

auth_bp = Blueprint("auth", __name__)




@auth_bp.route("/sign_up", methods=["POST"])
def sign_up():
    # Get and parse user_input
    user_input = request.get_json()

    if not user_input:
            return ApiResponse.error(
                message="No data provided",
                status_code=400
            )
    # Create user repository object 
    user_repository=UserRepository(db.session)
    #create auth service object 
    auth_service=AuthService(userrepository=user_repository)
    try:
        registration_results= auth_service.register_user(user_input)
        user=registration_results["user"]
        access_token=registration_results["access_token"]

        return ApiResponse.success(
            data={
                "id": user.id,
                "email_address": user.email_address,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token":access_token
            },
            message="User registered successfully",
            status_code=201
        )

    except ValidationError as e:
        return ApiResponse.error(
            message="Validation failed",
            errors=e.messages,
            status_code=400
        )

    except ConflictError as e:
        return ApiResponse.error(
            message=str(e),
            status_code=409
        )

    except Exception as e:
        traceback.print_exc()
        return ApiResponse.error(
            errors=str(e.orig),
            message="User registration failed",
            status_code=500
        )


@auth_bp.route("/sign_in", methods=["POST"])
def sign_in():
    # Get login data
    login_input = request.get_json()

    if not login_input:
        return ApiResponse.error(
            message="No data provided",
            status_code=400
        )

    # Initialize dependencies
    user_repository = UserRepository(db.session)
    auth_service = AuthService(userrepository=user_repository)

    try:
        login_results = auth_service.login_user(login_input)

        user = login_results["user"]
        access_token = login_results["access_token"]

        return ApiResponse.success(
            data={
                "id": user.id,
                "email_address": user.email_address,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "access_token": access_token
            },
            message="Login successful",
            status_code=200
        )

    except ValidationError as e:
        return ApiResponse.error(
            message="Validation failed",
            errors=e.messages,
            status_code=400
        )

    except AuthenticationError as e:
        return ApiResponse.error(
            message=str(e),
            status_code=401
        )

    except Exception as e:
        traceback.print_exc()
        return ApiResponse.error(
            message="Login failed",
            status_code=500
        )