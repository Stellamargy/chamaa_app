#ABSTRACTS USER MODEL DATABASE OPERATIONS 
from server.models.user import User
 
class UserRepository:

    def __init__(self, session):
        self.session = session
    # Checks if user is unique
    #Returns None if unique 
    #Returns user if not unique(user exist)
    def get_user_by_email(self, email_address):
        return self.session.query(User).filter_by(
            email_address=email_address
        ).first()
    #Instatiate a User instance from user input 
    #Persist the user instance attributes in db 
    def create_user(self, user_data):
        user_password = user_data.pop("password")
        user = User(**user_data)
        user.password = user_password

        try:
            self.session.add(user)
            self.session.flush()  
            self.session.commit()
            return user
        except Exception as e:
            self.session.rollback()
            raise  # Re-raises the same exception
        


