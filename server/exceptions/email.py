from server.exceptions.base import AppError
# ─────────────────────────────────────────────
#  Email
# ─────────────────────────────────────────────

class EmailError(AppError):
    """Base class for all email-related errors."""

class EmailDeliveryError(EmailError):
    """Raised when an email fails to be delivered to the recipient."""

