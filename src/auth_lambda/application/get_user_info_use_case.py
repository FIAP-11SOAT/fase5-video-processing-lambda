"""
Get User Info Use Case - Retrieve user information business logic
"""
from ..domain.entities import User
from ..domain.repositories import IAuthRepository

class GetUserInfoUseCase:
    """Use case for retrieving user information"""
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, access_token: str) -> User:
        """
        Get user information from access token
        
        Args:
            access_token: The access token
            
        Returns:
            User entity
            
        Raises:
            InvalidTokenException: If token is invalid
        """
        if not access_token:
            raise ValueError("Access token is required")
        
        return self.auth_repository.get_user_info(access_token)
