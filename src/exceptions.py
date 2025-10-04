"""KeshFlip SDK exceptions"""


class KeshFlipError(Exception):
    """Base exception for all KeshFlip SDK errors"""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response = response


class AuthenticationError(KeshFlipError):
    """Raised when authentication fails"""

    pass


class ValidationError(KeshFlipError):
    """Raised when request validation fails"""

    pass


class APIError(KeshFlipError):
    """Raised when API returns an error"""

    pass


class NetworkError(KeshFlipError):
    """Raised when network communication fails"""

    pass


class WebhookValidationError(KeshFlipError):
    """Raised when webhook signature validation fails"""

    pass
