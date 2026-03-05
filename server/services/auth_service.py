from server.schema import user_schema,login_schema
from sqlalchemy.exc import IntegrityError
from server.exceptions import ConflictError,AuthenticationError
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

    #Logs in a user 
    def login_user(self,login_credentials):
        #Validate login credentials
        valid_login_credentials=login_schema.load(login_credentials)
        #If valid credentials use email_address in credentials to fetch user from db
        existing_user=self.userrepository.get_user_by_email(
            valid_login_credentials["email_address"]
            )
        if not existing_user or not existing_user.check_password(
            valid_login_credentials["password"]
            ):
            raise AuthenticationError('Invalid credentials')
        
        #If credentials are valid - generate  access_token 
        jwt_service=JwtService(Config.ACCESS_TOKEN_SECRET)
        access_token=jwt_service.create_access_token(
            user_id=existing_user.id,
            is_verified=existing_user.is_verified,
            is_active=existing_user.is_active
            )
        return {
            "access_token":access_token,
            "user":existing_user
        }

            
            

          


            

        
    