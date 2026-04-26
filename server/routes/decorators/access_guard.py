#Acess guards -user states 
from functools import wraps
from flask_jwt_extended import get_jwt
from server.utilis.api_response import ApiResponse
from server.exceptions.auth import VerificationError,AuthenticationError


def require_user_state(verified=True, active=True):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()

            if active and not claims.get("user_active"):
                raise AuthenticationError("Your Account is inactive,Please contant support")

            if verified and not claims.get("email_verified"):
               raise VerificationError("Your email is not verified.Please verify your email address")

            return fn(*args, **kwargs)
        return wrapper
    return decorator