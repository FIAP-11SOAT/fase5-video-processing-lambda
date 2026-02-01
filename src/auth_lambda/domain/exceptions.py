class DomainException(Exception):
    pass


class UserAlreadyExistsException(DomainException):
    pass


class InvalidCredentialsException(DomainException):
    pass


class UserNotFoundException(DomainException):
    pass


class InvalidTokenException(DomainException):
    pass


class AuthenticationException(DomainException):
    pass
