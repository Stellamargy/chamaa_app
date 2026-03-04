import jwt
from datetime import datetime, timedelta, timezone


class JwtService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def _generate(self, payload: dict, expires_minutes: int) -> str:
        # Generic JWT generator used internally by all token types.
        now = datetime.now(timezone.utc)
        payload_copy = payload.copy()
        payload_copy.update({
            "iat": now,
            "exp": now + timedelta(minutes=expires_minutes)
        })
        return jwt.encode(payload_copy, self.secret_key, algorithm=self.algorithm)

    def create_access_token(
        self,
        user_id: int,
        # role: str,
        is_verified: bool,
        is_active: bool ,
        expires_minutes: int = 60
    ) -> str:
        
        # Creates an access token.
        # `is_verified` and `is_active` are UI/UX hints only.
        
        payload = {
            "sub": user_id,
            "type": "access",
            "is_verified": is_verified,  # UI hint only
            "is_active": is_active       # UI hint only
        }
        return self._generate(payload, expires_minutes)

    