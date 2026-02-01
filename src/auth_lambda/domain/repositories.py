from abc import ABC, abstractmethod
from typing import Optional

from src.auth_lambda.domain.entities import AuthToken, User


class IAuthRepository(ABC):

    @abstractmethod
    def register_user(self, username: str, password: str, email: Optional[str] = None) -> User:
        pass
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> AuthToken:
        pass
    
    @abstractmethod
    def get_user_info(self, access_token: str) -> User:
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        pass
