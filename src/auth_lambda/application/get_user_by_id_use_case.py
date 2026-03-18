import os
from base64 import b64encode

from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.repositories import IAuthRepository
from src.auth_lambda.domain.exceptions import InvalidTokenException

class GetUserByIdUseCase:
    
    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    @staticmethod
    def validate_ms_token(ms_token: str) -> bool:
        user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
        client_id = os.environ.get("COGNITO_USER_POOL_CLIENT_ID")
        if not user_pool_id or not client_id:
            return False
        expected = b64encode(f"{user_pool_id}:{client_id}".encode()).decode()
        return ms_token == expected

    def execute(self, ms_token: str, user_id: str) -> User:
        if not ms_token:
            raise ValueError("MS token is required")
        if not self.validate_ms_token(ms_token):
            raise InvalidTokenException("Invalid MS token")
        if not user_id:
            raise ValueError("User ID is required")
        
        return self.auth_repository.get_user_by_id(user_id)