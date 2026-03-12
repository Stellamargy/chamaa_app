from server.models import db
from server.repositories.user_repository import UserRepository
from server.services.auth_service import AuthService
from server.services.email_service import EmailService
from server.services.jwt_service import JwtService
from server.config import Config


def get_auth_service():

    user_repository = UserRepository(db.session)

    email_service = EmailService(
        smtp_host=Config.SMTP_HOST,
        smtp_port=Config.SMTP_PORT,
        smtp_from_address=Config.SMTP_FROM_ADDRESS,
        smtp_password=Config.SMTP_PASSWORD,
    )

    jwt_service = JwtService()

    return AuthService(
        user_repository=user_repository,
        email_service=email_service,
        jwt_service=jwt_service,
    )
