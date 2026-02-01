from base64 import b64encode
import os

from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.repositories import IAuthRepository



class GetUserInfoUseCase:

    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    @staticmethod
    def validate_token(access_token: str) -> bool:
        user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
        client_id = os.environ.get("COGNITO_CLIENT_ID")
        if not user_pool_id or not client_id:
            return False
        expected_token = b64encode(f"{user_pool_id}:{client_id}".encode()).decode()
        return access_token == expected_token


    def execute(self, access_token: str) -> User:
        if not access_token:
            raise ValueError("Access token is required")

        if not self.validate_token(access_token):
            raise ValueError("Invalid access token")

        return self.auth_repository.get_user_info(access_token)
