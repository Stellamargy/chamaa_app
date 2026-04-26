from logging import getLogger
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from server.schema import user_schema, login_schema
from server.exceptions.database import ResourceConflictError
from server.exceptions.email import EmailDeliveryError
from server.exceptions.auth import AuthenticationError
from server.exceptions.database import ResourceNotFoundError ,DatabaseError
from server.exceptions.auth import VerificationError
from server.exceptions.auth import AuthorizationError

logger = getLogger(__name__)


class AuthService:

    def __init__(self, user_repository, email_service, jwt_service,db_session):
        self.user_repository = user_repository
        self.email_service = email_service
        self.jwt_service = jwt_service
        self.db_session=db_session

    # Public methods

    # Register a user
    def register_user(self, user_data):
        #1. validate user registration  data
        #
        valid_user_data = user_schema.load(user_data)
        #2 .Create user record and access token
        user, access_token = self._create_user(valid_user_data)
        # Send verification email
        email_sent = self._send_verification_email(user)
        return {
            "user": user,
            "access_token": access_token,
            "verification_email_sent": email_sent,
        }

    # Logs in user
    def login_user(self, login_credentials):
        # validates login credeentials .
        valid_credentials = login_schema.load(login_credentials)
        #get user using the provided email .
        user = self.user_repository.get_user_by_email(
            valid_credentials["email_address"]
        )
        # Check credentials
        if not user or not user.check_password(valid_credentials["password"]):
            raise AuthenticationError("Failed to authenticate .Please try again")
        # Generate access tokens
        access_token = self.jwt_service.generate_access_token(user)
        return {"user": user, "access_token": access_token}

    # Send email verification
    #This is supposed to be send_verification email
    def resend_verification_email(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise ResourceNotFoundError("Account not found.Please contact support")
        if not user.is_active:
            raise AuthorizationError("Your account has been deactivated. Please contact support.")
        if user.email_verified:
            raise VerificationError("Your email is already verified.")

        #Results to True or False 
        email_sent=self._send_verification_email(user)
        if not email_sent:
            raise EmailDeliveryError("We couldn’t send the email. Please try again later.") from e
        return email_sent

    # Verify email address
    def verify_email(self, token):
        payload = self.jwt_service.decode_email_verification_token(token)
        user_id = int(payload["sub"])
        user = self.user_repository.get_user_by_id(user_id)

        if not user:
            raise AuthenticationError("Authentication failed")
        if user.email_verified:
           raise VerificationError("Your email is already verified.")

        try:
             user.email_verified=True
             #generate new access token-prevent stale token
             access_token=self.jwt_service.generate_access_token(user=user)
             self.db_session.commit()
             
             return {
                "user":user,
                "access_token":access_token
             }
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise DatabaseError("Failed to verify email try again later") from e
        # self._commit(
        #     error_message="Unable to verify email.Please request for a new verification link."
        #     )
         #This has to return an access token because email is being verified .(STALE ACCESS TOKEN)   
        

    # Private helpers methods 

    # Persist user to db  and create access token
    def _create_user(self, valid_user_data):
        try:
            user = self.user_repository.save_user(valid_user_data)
            access_token = self.jwt_service.generate_access_token(user)
            self.user_repository.db_session.commit()
            return user, access_token

        except IntegrityError as e:
            self.user_repository.db_session.rollback()
            #Only works on postgress db (cons incase db change)-Future note
            error_message = str(e.orig)
            if "email_address" in error_message or "phone_number" in error_message:
                raise ResourceConflictError("Account already exists, kindly sign in.") from e
            raise DatabaseError("We couldn’t save your information. Please try again.") from e
        except SQLAlchemyError as e:
            self.user_repository.db_session.rollback()
            raise DatabaseError("We couldn’t save your information. Please try again.") from e

    # Send  verification email
    def _send_verification_email(self, user):
        try:
            #Create email verification token 
            verify_token = self.jwt_service.create_email_verification_token(user.id)
            #Create email body
            email_body = self.email_service.generate_verification_email(
                user=user, verify_email_token=verify_token
            )
            #send email verification email .
            result = self.email_service.send_email(
                to=user.email_address,
                subject="Verify your email address",
                html_body=email_body,
            )
            return result.get("success", False)

        except EmailDeliveryError as e:
            logger.error("Verification email failed for user ", user.id, exc_info=True)
            return False
           

    def _commit(self, error_message="A database error occurred"):
        try:
            self.user_repository.db_session.commit()
        except SQLAlchemyError as e:
            self.user_repository.db_session.rollback()
            raise DatabaseError(error_message) from e
