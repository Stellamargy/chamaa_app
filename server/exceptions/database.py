from server.exceptions.base import AppError
# ─────────────────────────────────────────────
#  Database
# ─────────────────────────────────────────────
class DatabaseError(AppError):
    """Raised when something goes wrong interacting with the database."""

class ResourceConflictError(DatabaseError):
    """Raised when a resource conflicts with an existing database record."""

class ResourceNotFoundError(DatabaseError):
    """Raised when a resource does not exist in database"""

