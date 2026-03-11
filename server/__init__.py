from flask import Flask
from server.models import db
from server.models.user import User
from .config import Config 
from server.routes.auth import auth_bp
from .extensions import jwt
from server.errors.error_handlers import register_error_handlers

def create_app():

    #Create flask app instance 
    app=Flask(__name__)

    #Load configurations 
    app.config.from_object(Config)

    # initialize extensions 
    db.init_app(app)
    jwt.init_app(app)   

    #register bluerints 
    app.register_blueprint(auth_bp, url_prefix="/auth")
    # register error handler
    register_error_handlers(app)

    
    return app