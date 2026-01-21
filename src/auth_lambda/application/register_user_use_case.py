"""
Register User Use Case - User registration business logic
"""
from typing import Optional
from ..domain.entities import User
from ..domain.repositories import IAuthRepository


class RegisterUserUseCase:
    """Use case for user registration"""
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, username: str, password: str, email: Optional[str] = None) -> User:
        """
        Register a new user
        
        Args:
            username: The username for the new user
            password: The password for the new user
            email: Optional email address
            
        Returns:
            User entity
            
        Raises:
            UserAlreadyExistsException: If username already exists
        """
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        return self.auth_repository.register_user(username, password, email)
