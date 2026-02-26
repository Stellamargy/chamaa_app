from server.models import db
from server.repositories.user_repository import UserRepository
from server.services.user_registration_service import UserRegistrationService

def get_user_registration_service():
    repo = UserRepository(db.session)  
    return UserRegistrationService(repo)