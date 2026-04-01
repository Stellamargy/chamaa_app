class AppError(Exception):
    """Root exception for the entire application."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
