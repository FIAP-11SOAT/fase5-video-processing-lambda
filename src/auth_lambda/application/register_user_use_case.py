from typing import Optional

from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.repositories import IAuthRepository


class RegisterUserUseCase:

    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, username: str, password: str, email: Optional[str] = None) -> User:
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        return self.auth_repository.register_user(username, password, email)
