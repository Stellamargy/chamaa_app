from flask import Blueprint
from flask_restful import Api
from server.resources.auth import RegisterResource,LoginResource


auth_bp=Blueprint("auth",__name__)
api=Api(auth_bp)

api.add_resource(RegisterResource,"/sign_up")
api.add_resource(LoginResource,"/sign_in")