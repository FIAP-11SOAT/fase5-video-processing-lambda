from typing import Any

from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.repositories import IAuthRepository
from src.auth_lambda.domain.exceptions import InvalidTokenException

class GetUserInfoUseCase:

    def __init__(self, auth_repository: IAuthRepository):
        self.auth_repository = auth_repository

    def execute(self, access_token: str) -> User:
        if not access_token:
            raise ValueError("Access token is required")

        return self.auth_repository.get_user_info(access_token)
