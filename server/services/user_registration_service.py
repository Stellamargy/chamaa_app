from server.schema import user_schema
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from server.exceptions import ConflictError

class UserRegistrationService:

    def __init__(self,userrepository):
        self.userrepository=userrepository

    #This function is primarily used to create a user record(signing up)
    def create_user_account(self,user_data):
        # Validate registration input
        valid_user_data=user_schema.load(user_data)
        
        # Create user record - (register a user)
        try:
            user=self.userrepository.add_user(valid_user_data)
            self.userrepository.db_session.commit()
        except IntegrityError as e:
            self.userrepository.db_session.rollback()
            if "email_address" in str(e.orig):
                raise ConflictError("Account already exists,kindly sign up")
            raise
        except Exception as e:
            self.userrepository.db_session.rollback()
            raise

        return user

       
        