from server.models import db
from server.repositories.user_repository import UserRepository
from server.services.auth_service import AuthService
from server.services.email_service import EmailService
from server.services.jwt_service import JwtService
from server.config import Config

#chama
from server.repositories.chama import ChamaRepository
from server.repositories.chama_member import ChamaMemberRepository
from server.repositories.chama_wallet import ChamaWalletRepository
from server.services.chama_service import ChamaService

db_session = db.session
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
        db_session=db_session
    )

def get_chama_service():
   
    chama_repository = ChamaRepository(db_session)
    chama_member_repository = ChamaMemberRepository(db_session)
    chama_wallet_repository = ChamaWalletRepository(db_session)
    user_repository=UserRepository(db_session=db_session)

    return ChamaService(
        db_session=db_session,
        chama_repository=chama_repository,
        chama_member_repository=chama_member_repository,
        chama_wallet_repository=chama_wallet_repository,
        user_repository=user_repository
    )


