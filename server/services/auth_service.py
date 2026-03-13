from logging import getLogger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from server.schema import user_schema, login_schema
from server.exceptions import (
    ConflictError,
    AuthenticationError,
    DatabaseError,
    EmailDeliveryError,
    EmailConfigurationError,
)

logger = getLogger(__name__)


class AuthService:

    def __init__(self, user_repository, email_service, jwt_service):
        self.user_repository = user_repository
        self.email_service = email_service
        self.jwt_service = jwt_service

    # Public methods

    # Register a user
    def register_user(self, user_data):
        # validate user registration  data
        valid_user_data = user_schema.load(user_data)
        # Create user record and access token
        user, access_token = self._create_user(valid_user_data)
        # Send verification email
        email_sent = self._send_verification_email(user)
        return {
            "user": user,
            "access_token": access_token,
            "verification_email_sent": email_sent,
        }

    # Logs in (aauthenticate) user
    def login_user(self, login_credentials):
        # validates login credeentials
        valid_credentials = login_schema.load(login_credentials)
        user = self.user_repository.get_user_by_email(
            valid_credentials["email_address"]
        )
        # Check credentials
        if not user or not user.check_password(valid_credentials["password"]):
            raise AuthenticationError("Invalid email address or password")
        # Generate access tokens
        access_token = self.jwt_service.generate_access_token(user)
        return {"user": user, "access_token": access_token}

    # Send email verification
    def resend_verification_email(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise AuthenticationError("Invalid authentication credentials")
        if not user.is_active:
            raise AuthenticationError("Account deactivated")
        if user.is_verified:
            raise ConflictError("User already verified")

        return self._send_verification_email(user)

    # Verify email address
    def verify_email(self, token):
        payload = self.jwt_service.decode_email_verification_token(token)
        user_id = int(payload["sub"])
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise AuthenticationError("Invalid verification token")
        if user.is_verified:
            raise ConflictError("Email already verified")

        user.is_verified = True
        self._commit(error_message="Failed to verify email")
        return user

    # Private helpers
    # Persist user to db  and create access token
    def _create_user(self, valid_user_data):
        try:
            user = self.user_repository.save_user(valid_user_data)
            access_token = self.jwt_service.generate_access_token(user)
            self.user_repository.db_session.commit()
            return user, access_token

        except IntegrityError as e:
            self.user_repository.db_session.rollback()
            error_message = str(e.orig)
            if "email_address" in error_message or "phone_number" in error_message:
                raise ConflictError("Account already exists, kindly sign in.") from e
            raise DatabaseError("A database constraint was violated") from e

        except SQLAlchemyError as e:
            self.user_repository.db_session.rollback()
            raise DatabaseError("A database error occurred") from e

    # Send  verification email
    def _send_verification_email(self, user):
        try:
            verify_token = self.jwt_service.create_email_verification_token(user.id)
            html_body = self.email_service.generate_verification_email(
                user=user, verify_email_token=verify_token
            )
            result = self.email_service.send_email(
                to=user.email_address,
                subject="Verify your email address",
                html_body=html_body,
            )
            return result.get("success", False)

        except (EmailDeliveryError, EmailConfigurationError) as e:
            logger.error("Verification email failed for user %s: %s", user.id, e)
            return False

    def _commit(self, error_message="A database error occurred"):
        try:
            self.user_repository.db_session.commit()
        except SQLAlchemyError as e:
            self.user_repository.db_session.rollback()
            raise DatabaseError(error_message) from e
