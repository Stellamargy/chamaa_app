from server.dependecies import get_user_registration_service
from server.utilis.api_response import ApiResponse
from flask import Blueprint, request
from marshmallow import ValidationError
from server.exceptions import ConflictError

auth_bp = Blueprint("auth", __name__)




@auth_bp.route("/register", methods=["POST"])
def register():

    try:
        user_input = request.get_json()

        if not user_input:
            return ApiResponse.error(
                message="No data provided",
                status_code=400
            )
        user_registration_service=get_user_registration_service()
        user = user_registration_service.create_user_account(user_input)

        return ApiResponse.success(
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
        
        return ApiResponse.error(
            errors=str(e),
            message="Internal Server Error",
            status_code=500
        )
