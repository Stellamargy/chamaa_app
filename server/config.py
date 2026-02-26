# Purpose - Manages app configuration centrally 

#IMPORTS
from dotenv import load_dotenv
import os

load_dotenv()  # reads variables from a .env file and sets them in os.environ


#Class to manage configuration 
class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI")
    SMTP_PASSWORD=os.getenv("SMTP_PASSWORD")
    SMTP_FROM_ADDRESS=os.getenv("SMTP_FROM_ADDRESS") 
    SMTP_HOST=os.getenv("SMTP_HOST","smtp.gmail.com") 
    SMTP_PORT=int(os.getenv("SMTP_PORT",587) )
    EMAIL_VERIFICATION_KEY=os.getenv("EMAIL_VERIFICATION_SECRETS")