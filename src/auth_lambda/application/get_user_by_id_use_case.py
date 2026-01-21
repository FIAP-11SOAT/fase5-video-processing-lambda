"""
Get User By ID Use Case - Retrieve user by ID business logic
"""
from ..domain.entities import User
from ..domain.repositories import IAuthRepository

class GetUserByIdUseCase:
    """Use case for retrieving user by ID"""
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, user_id: str) -> User:
        """
        Get user by their ID
        
        Args:
            user_id: The user ID
            
        Returns:
            User entity
            
        Raises:
            UserNotFoundException: If user not found
        """
        if not user_id:
            raise ValueError("User ID is required")
        
        return self.auth_repository.get_user_by_id(user_id)
