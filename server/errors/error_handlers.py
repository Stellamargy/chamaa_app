from flask import jsonify
from marshmallow import ValidationError
from server.exceptions.database import ResourceConflictError
from server.exceptions.database import DatabaseError
from server.utilis.api_response import ApiResponse
from server.exceptions.auth import AuthenticationError
from server.exceptions.database import ResourceNotFoundError
from server.exceptions.email import EmailDeliveryError
from server.exceptions.auth import VerificationError
from server.exceptions.base import AppError
from logging import getLogger

logger=getLogger(__name__)
def register_error_handlers(app):
    # Data validation
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):

        return ApiResponse.error(
            message="Data Input validation failed", errors=e.messages, status_code=400
        )

    @app.errorhandler(ResourceConflictError)
    def handle_resource_conflict_error(e):

        return ApiResponse.error(message=str(e), status_code=409)

    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_conflict_error(e):

        return ApiResponse.error(message=str(e), status_code=404)
   
    @app.errorhandler(AuthenticationError)
    def handle_auth_error(e):
        return ApiResponse.error(message=str(e), status_code=401)

    # Make database error message specific
    @app.errorhandler(DatabaseError)
    def handle_database_error(e):
        logger.error("Database error occurred", exc_info=True)
        return ApiResponse.error(message=str(e), status_code=500)
   
    @app.errorhandler(AppError)
    def handle_unexpected_error(e):

        logger.error("A server error occurred", exc_info=True)
        return ApiResponse.error(
            message="An unexpected error occurred. Please try again later.", status_code=500
        )

    @app.errorhandler(EmailDeliveryError)
    def handle_email_delivery_error(e):
        logger.error("Email error occurred", exc_info=True)
        return ApiResponse.error(message=str(e), status_code=500)

   

    @app.errorhandler(VerificationError)
    def handle_verification_error(e):

        return ApiResponse.error(message=str(e), status_code=403)
    
  
