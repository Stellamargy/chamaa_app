import jwt
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token
from flask import current_app
class JwtService:
    # Create a JWT access token for the given user.
    @staticmethod
    def generate_access_token(user):
        try:
            return create_access_token(
                identity=str(user.id),
                additional_claims={
                    "email_verified": user.is_verified,
                    "user_active": user.is_active
                }
            )

        except Exception as e:
            # preserve original error for logging
            raise RuntimeError("Failed to generate access token") from e

    # Create email verification token    
    @staticmethod
    def create_email_verification_token(user_id):

        payload = {
            "sub": str(user_id),
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24),
            "iat":datetime.now(tz=timezone.utc),
            "type": "email_verification"
        }

        try:
            token = jwt.encode(
            payload,
            current_app.config["EMAIL_VERIFICATION_SECRET"],
            algorithm="HS256"
            )
            return token
        except Exception as e:
            raise RuntimeError("Failed to generate access token") from e

        