from flask_restful import Resource
from flask import request ,jsonify
from marshmallow import  ValidationError
# class RegisterResource(Resource):
#     def __init__(self,user_registration_service):
#         self.user_registration_service=user_registration_service


#     def post(self):
#         try:
#             # Get json (user data) from request object
#             user_input=request.get_json()   # Returns dict / None 
#             if not user_input:
#                 # Return http response if no user input from request
#                 return jsonify(
#                     {
#                         "status":"error",
#                         "error":"No data provided"
#                     }
#                 ) , 400
#             user=self.user_registration_service.onboard_user(user_input)

#             # Return success response
#             return {
#                 "status":"success",
#                 "message": "User registered successfully",
#                 "data": {
#                     "id": user.id,
#                     "email_address": user.email_address,
#                     "first_name": user.first_name,
#                     "last_name": user.last_name
#                 }
#             }, 201

#         except ValidationError as e:
#             # Marshmallow validation failed
#             return jsonify(
#                 {
#                     "status":"error",
#                     # "error":e.messages,

#                 }
#             ),400
            
#         except ConflictError as e:
#             # Email already exists
#             return jsonify(
#                 {
#                     "status":"error",
#                     "error":str(e),

#                 }
#             ),409
            
#         except Exception as e:
#             # Unexpected error
#             print(f"Error: {e}")  # Log it
#             return jsonify(
#                 {
#                     "status":"error",
#                     "error":"Internal Server error",

#                 }
#             ),500


class RegisterResource(Resource):

    def __init__(self, user_registration_service):
        self.user_registration_service = user_registration_service

    def post(self):
        try:
            user_input = request.get_json()

            if not user_input:
                return {
                    "status": "error",
                    "error": "No data provided"
                }, 400

            user = self.user_registration_service.onboard_user(user_input)

            return {
                "status": "success",
                "message": "User registered successfully",
                "data": {
                    "id": user.id,
                    "email_address": user.email_address,
                    "first_name": user.first_name,
                    "last_name": user.last_name
                }
            }, 201

        except ValidationError as e:
            return {
                "status": "error",
                "error": e.messages
            }, 400

        except ConflictError as e:
            return {
                "status": "error",
                "error": str(e)
            }, 409

        except Exception as e:
            print(f"Error: {e}")
            return {
                "status": "error",
                "error": "Internal Server Error"
            }, 500














class LoginResource(Resource):
    def post(self):
        pass
