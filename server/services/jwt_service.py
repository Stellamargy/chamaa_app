import jwt
from datetime import datetime, timedelta, timezone


class JwtService:
    def __init__(self, secret_key, algorithm="HS256", default_exp_minutes=15):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.default_exp_minutes = default_exp_minutes
    # Generates and return JWT token 
    def generate_token(self, payload: dict, expires_in: int | None = None):
        expiry = datetime.now(timezone.utc) + timedelta(
            minutes=expires_in or self.default_exp_minutes
        )

        payload_copy = payload.copy()
        payload_copy["exp"] = expiry

        token = jwt.encode(
            payload_copy,
            self.secret_key,
            algorithm=self.algorithm
        )

        return token

 






