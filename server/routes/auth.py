from flask import Blueprint
from flask_restful import Api
from server.resources.auth import RegisterResource,LoginResource
from server.repositories.user_repository import UserRepository
from server.services.user_registration import UserRegistration
from server.models import db 


auth_bp=Blueprint("auth",__name__)
api=Api(auth_bp)
# Set up dependecies 
user_repository=UserRepository(db.session)
user_registration_service=UserRegistration(user_repository)


api.add_resource(
    RegisterResource,
    "/sign_up",
    resource_class_kwargs={'user_registration_service': user_registration_service}
)
api.add_resource(LoginResource,"/sign_in")