from server.exceptions.base import AppError
# ─────────────────────────────────────────────
#  Authentication & Authorization
# ─────────────────────────────────────────────

class AuthError(AppError):
    """Base class for authentication and authorization errors."""

class AuthenticationError(AuthError):
    """Raised when credentials are missing or invalid."""

class AuthorizationError(AuthError):
    """Raised when an authenticated user lacks permission to perform an action."""

class VerificationError(AuthError):
    """Raised when a verification step fails (e.g. email token, OTP)."""
