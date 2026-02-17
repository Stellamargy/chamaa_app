from server.repositories.user_repository import UserRepository
from server.services.user_registration import UserRegistration
from server.utilis.api_response import ApiResponse
from server.models import db  
from flask import Blueprint, request
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)

# Create dependencies 
user_repository=UserRepository(db.session)
user_registration_service = UserRegistration(user_repository)
api_response=ApiResponse()

@auth_bp.route("/register", methods=["POST"])
def register():

    try:
        user_input = request.get_json()

        if not user_input:
            return ApiResponse.error(
                message="No data provided",
                status_code=400
            )

        user = user_registration_service.onboard_user(user_input)

        return api_response.success(
            data={
                "id": user.id,
                "email_address": user.email_address,
                "first_name": user.first_name,
                "last_name": user.last_name
            },
            message="User registered successfully",
            status_code=201
        )

    except ValidationError as e:
        return api_response.error(
            message="Validation failed",
            errors=e.messages,
            status_code=400
        )

    except ConflictError as e:
        return api_response.error(
            message=str(e),
            status_code=409
        )

    except Exception as e:
        print(f"Unexpected error: {e}")
        return api_response.error(
            message="Internal Server Error",
            status_code=500
        )
