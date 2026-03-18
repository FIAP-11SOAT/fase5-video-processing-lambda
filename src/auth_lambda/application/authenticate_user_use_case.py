from src.auth_lambda.domain.entities import AuthToken
from src.auth_lambda.domain.repositories import IAuthRepository


class AuthenticateUserUseCase:
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository
    
    def execute(self, username: str, password: str) -> AuthToken:
        if not username or not password:
            raise ValueError("Username and password are required")
        
        return self.auth_repository.authenticate(username, password)
