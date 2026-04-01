from server.exceptions.base import AppError
# ─────────────────────────────────────────────
#  User
# ─────────────────────────────────────────────
class UserError(AppError):
    """Base class for all user-related errors."""

class UserAlreadyExistsError(UserError):
    """Raised when attempting to create a user that already exists."""

class UserNotFoundError(UserError):
    """Raised when a requested user cannot be found."""
