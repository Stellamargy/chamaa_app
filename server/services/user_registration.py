from server.schema.userschema import UserSchema
from server.exceptions import ConflictError
from marshmallow import ValidationError
# from server.repositories.user_repository import UserRepository
class UserRegistration:
    def __init__(self,userrepository):
        #be able to access the object as an attribute . 
        #be able to access the object methods too .
        self.userrepository=userrepository
    
    def onboard_user(self,user_data):
        # Use schema to validate user input / data
        user_schema=UserSchema() 
        valid_user_data=user_schema.load(user_data)
        
        #Check if user is unique  
        existing_user= self.userrepository.get_user_by_email(valid_user_data["email_address"])
        # If they exist 
        if existing_user:
            raise ConflictError("Email already exist")

         #If user is unique - persist them (add them to db )
       
        user=self.userrepository.create_user(valid_user_data)

        return user 
        

        

        
        

        

# data={
#   "first_name": "Brian",
#   "last_name": "Otieno",
#   "password": "pa55word",
#   "email_address": "brian.Otieno@gmail.com   "
# }

# user_registration =UserRegistration()
# try:
#     user=user_registration.onboard_user(data)
#     print(type(user))
# except ValidationError as error:
#     print(error.messages)

