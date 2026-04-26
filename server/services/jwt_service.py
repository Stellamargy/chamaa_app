import jwt
from jwt import ExpiredSignatureError
from server.exceptions.auth import VerificationError
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token
from flask import current_app


class JwtService:
    # Create  access token
    @staticmethod
    def generate_access_token(user):
        return create_access_token(
                identity=str(user.id),
                additional_claims={
                    "email_verified": user.email_verified,
                    "user_active": user.is_active,
                },
            )
        
            
    # Create email verification token
    @staticmethod
    def create_email_verification_token(user_id):

        payload = {
            "sub": str(user_id),
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24),
            "type": "email_verification",
        }
        token = jwt.encode(
                payload,
                current_app.config["EMAIL_VERIFICATION_SECRET"],
                algorithm="HS256",
            )
        return token

       
    # Checks email verification token validility   
    @staticmethod
    def decode_email_verification_token(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config["EMAIL_VERIFICATION_SECRET"],
                algorithms=["HS256"],
            )

            if payload.get("type") != "email_verification":
                raise VerificationError("This verification link is invalid. Please request a new one.")

            return payload

        except jwt.ExpiredSignatureError as e:
            raise VerificationError("This verification link has expired. Please request a new one.") from e

        except jwt.InvalidTokenError as e:
            raise VerificationError("This verification link is invalid. Please request a new one.") from e
