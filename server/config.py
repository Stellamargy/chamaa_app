# Purpose - Manages app configuration centrally 

#IMPORTS
from dotenv import load_dotenv
import os

load_dotenv()  # reads variables from a .env file and sets them in os.environ


#Class to manage configuration 
class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URI")