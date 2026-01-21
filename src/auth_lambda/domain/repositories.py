"""
Repository interfaces - Abstract definitions for data access
Following Dependency Inversion Principle
"""
from abc import ABC, abstractmethod
from typing import Optional
from .entities import User, AuthToken


class IAuthRepository(ABC):
    """Interface for authentication operations"""
    
    @abstractmethod
    def register_user(self, username: str, password: str, email: Optional[str] = None) -> User:
        """Register a new user"""
        pass
    
    @abstractmethod
    def authenticate(self, username: str, password: str) -> AuthToken:
        """Authenticate user and return tokens"""
        pass
    
    @abstractmethod
    def get_user_info(self, access_token: str) -> User:
        """Get user information from access token"""
        pass
    
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        """Get user by their ID"""
        pass
