class ConflictError(Exception):
    """Raised when a resource conflicts with existing data"""
    pass

class AuthenticationError(Exception):
    """Raised when authentication fails"""
    pass
