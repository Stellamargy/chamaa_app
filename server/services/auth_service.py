from server.schema import user_schema
from sqlalchemy.exc import IntegrityError
from server.exceptions import ConflictError
from .jwt_service import JwtService
from server.config import Config
class AuthService:
    def __init__(self,userrepository):
        self.userrepository=userrepository
    
    # Register a user 
    def register_user(self,user_data):
        #use user schema for data validation 
        valid_user_data=user_schema.load(user_data)
        
        # Create user record 
        try:
            user=self.userrepository.create_user(valid_user_data)
             #create access token 
            jwt_service=JwtService(Config.ACCESS_TOKEN_SECRET)
            access_token=jwt_service.create_access_token(user_id=user.id,is_verified=user.is_verified,is_active=user.is_active)
            self.userrepository.db_session.commit()
        except IntegrityError as e:
            self.userrepository.db_session.rollback()
            if "email_address" in str(e.orig):
                raise ConflictError("Account already exists,kindly sign in")
            if "phone_number" in str(e.orig):
                raise ConflictError("Account already exists,kindly sign in")
            raise
        except Exception as e:
            self.userrepository.db_session.rollback()
            raise

       

        return {
            "user":user,
            "access_token":access_token
        }
        
    