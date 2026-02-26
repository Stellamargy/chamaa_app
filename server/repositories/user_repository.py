#ABSTRACTS USER MODEL DATABASE OPERATIONS 
from server.models.user import User
 
class UserRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    #return None / existing user with the provided email
    def get_user_by_email(self, email_address):
        return self.db_session.query(User).filter_by(
            email_address=email_address
        ).first()

    #create a user record (add user) 
    def add_user(self, user_data):
        user_password = user_data.pop("password")
        user = User(**user_data)
        #use password setter to hash password
        user.password = user_password
        self.db_session.add(user)
        self.db_session.flush()
        return user
        
        


