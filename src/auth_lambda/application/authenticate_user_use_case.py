"""
Authenticate User Use Case - User authentication business logic
"""
from ..domain.entities import AuthToken
from ..domain.repositories import IAuthRepository

class AuthenticateUserUseCase:
    """Use case for user authentication"""
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, username: str, password: str) -> AuthToken:
        """
        Authenticate a user
        
        Args:
            username: The username
            password: The password
            
        Returns:
            AuthToken entity with access tokens
            
        Raises:
            InvalidCredentialsException: If credentials are invalid
        """
        if not username or not password:
            raise ValueError("Username and password are required")
        
        return self.auth_repository.authenticate(username, password)
