"""
Domain-specific exceptions
"""

class DomainException(Exception):
    """Base exception for domain layer"""
    pass

class UserAlreadyExistsException(DomainException):
    """Raised when trying to register a user that already exists"""
    pass

class InvalidCredentialsException(DomainException):
    """Raised when authentication credentials are invalid"""
    pass

class UserNotFoundException(DomainException):
    """Raised when user is not found"""
    pass

class InvalidTokenException(DomainException):
    """Raised when token is invalid or expired"""
    pass

class AuthenticationException(DomainException):
    """Generic authentication exception"""
    pass
