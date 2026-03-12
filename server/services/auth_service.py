from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from server.schema import user_schema, login_schema
from server.exceptions import ConflictError, AuthenticationError, DatabaseError


class AuthService:
    # Inject dependecies
    def __init__(self, user_repository, email_service, jwt_service):
        self.user_repository = user_repository
        self.email_service = email_service
        self.jwt_service = jwt_service

    # Register a user
    def register_user(self, user_data):
        # Validate user registration input
        valid_user_data = user_schema.load(user_data)

        try:
            # create user record
            user = self.user_repository.save_user(valid_user_data)
            # create access token
            access_token = self.jwt_service.generate_access_token(user)
            # save user record to the db
            self.user_repository.db_session.commit()

            return {"user": user, "access_token": access_token}

        except IntegrityError as e:

            self.user_repository.db_session.rollback()

            error_message = str(e.orig)

            if "email_address" in error_message:
                raise ConflictError("Account already exists,kindly sign in.") from e

            if "phone_number" in error_message:
                raise ConflictError(
                    "Account already exists,kindly sign in."
                ) from e

            raise DatabaseError("A database constraint was violated") from e

        except SQLAlchemyError as e:

            self.user_repository.db_session.rollback()

            raise DatabaseError("A database error occurred") from e

    # Signs/logs in a user
    def login_user(self, login_credentials):
        # validate login credentials
        valid_credentials = login_schema.load(login_credentials)
        # Fetch a user from users table using the email in the provided login credentials .
        user = self.user_repository.get_user_by_email(
            valid_credentials["email_address"]
        )
        # Checks login credentials
        if not user or not user.check_password(valid_credentials["password"]):
            raise AuthenticationError("Invalid email or password")
        # generate access tokens
        access_token = self.jwt_service.generate_access_token(user)

        return {"user": user, "access_token": access_token}

    # send email verification link to user's email inbox
    def send_email_verification_link(self, user_id):

        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise AuthenticationError("Invalid authentication credentials")

        if not user.is_active:
            raise AuthenticationError("Account deactivated")

        if user.is_verified:
            raise ConflictError("User already verified")

        verify_token = self.jwt_service.create_email_verification_token(user.id)

        verification_email = self.email_service.generate_verification_email(
            user=user, verify_email_token=verify_token
        )

        return self.email_service.send_email(
            to=user.email_address,
            subject="Verify your email",
            html_body=verification_email,
        )
