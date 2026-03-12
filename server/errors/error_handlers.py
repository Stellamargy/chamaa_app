from flask import jsonify
from marshmallow import ValidationError
from server.exceptions import (
    ConflictError,
    AuthenticationError,
    DatabaseError,
    EmailConfigurationError,
    EmailDeliveryError,
)
from server.utilis.api_response import ApiResponse


def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):

        return ApiResponse.error(
            message="Validation failed", errors=e.messages, status_code=400
        )

    @app.errorhandler(ConflictError)
    def handle_conflict_error(e):

        return ApiResponse.error(message=str(e), status_code=409)

    @app.errorhandler(AuthenticationError)
    def handle_auth_error(e):

        return ApiResponse.error(message=str(e), status_code=401)

    @app.errorhandler(DatabaseError)
    def handle_database_error(e):

        return ApiResponse.error(message="A server error occurred", status_code=500)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):

        # log full stacktrace internally
        import traceback

        traceback.print_exc()

        return ApiResponse.error(
            message="An unexpected error occurred", status_code=500
        )

    @app.errorhandler(EmailDeliveryError)
    def handle_email_delivery_error(e):

        return ApiResponse.error(message="Failed to send email", status_code=500)

    @app.errorhandler(EmailConfigurationError)
    def handle_email_configuration_error(e):

        return ApiResponse.error(
            message="Unable to send email,Try again later", status_code=502
        )
