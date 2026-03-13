class ConflictError(Exception):
    """Raised when a resource conflicts with existing database resource"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class DatabaseError(Exception):
    """Raised when something goes wrong when interacting with the database """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class EmailDeliveryError(Exception):
    """Raised when an email cannot be delivered to one or more recipients."""
    def __init__(self, message: str, failed_recipients: list = None):
        super().__init__(message)
        self.message = message
        self.failed_recipients = failed_recipients or []

class EmailConfigurationError(Exception):
    """Raised when the SMTP server is misconfigured or unreachable."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class VerificationError(Exception):
    """Raised when verification fails """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
