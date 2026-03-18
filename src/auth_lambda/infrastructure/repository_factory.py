from typing import Optional

from src.auth_lambda.domain.repositories import IAuthRepository
from src.auth_lambda.infrastructure.cognito_repository import CognitoRepository

_repository_instance: Optional[IAuthRepository] = None

def get_auth_repository() -> IAuthRepository:
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = CognitoRepository()
    return _repository_instance
