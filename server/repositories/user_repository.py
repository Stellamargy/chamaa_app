from server.models.user import User
 
class UserRepository:

    def __init__(self, db_session):
        self.db_session = db_session

    #If the provided email exist in users table , return existing user else None
    def get_user_by_email(self, email_address):
        return self.db_session.query(User).filter_by(
            email_address=email_address
        ).first()
    #If user_id exist return user if not None
    def get_user_by_id(self,user_id):
        return self.db_session.query(User).filter_by(
            id=user_id).first()

    #create a user record 
    def save_user(self, user_data):
        user_password = user_data.pop("password")
        user = User(**user_data)
        #use password setter to hash password
        user.password = user_password
        self.db_session.add(user)
        self.db_session.flush()
        return user
        
        


