from flask import Blueprint,request
from flask_jwt_extended import jwt_required, get_jwt
from server.utilis.api_response import ApiResponse
from server.services.service_factory import get_chama_service
from server.routes.decorators.access_guard import require_user_state

#create chama blueprint
chama_bp = Blueprint("chamas", __name__,url_prefix="/api/chamas")

# Any logged in user can access this endpoint 
@chama_bp.route("", methods=["POST"])
@jwt_required() #checks if there is a valid jwt in request headers
@require_user_state()
def create_chama():
    #Get chama details  from request 
    chama_input = request.get_json()
    if not chama_input:
        return ApiResponse.error(message="Chama's details is required", status_code=400)
    # Get current user id from JWT (get_jwt())
    user_id = int(get_jwt()["sub"])

    # Create chama using chama service 
    #1.Get chama service instance
    chama_service=get_chama_service()
    #2 Create chama 
    chama=chama_service.create_chama(chama_input=chama_input,current_user_id=user_id)
    # 3.Return chama created .
    return ApiResponse.success(
        data={
            "id":chama.id,
            "name":chama.name,
            "description":chama.description
        },
        message="Chama successfully created",
        status_code=201
    )


