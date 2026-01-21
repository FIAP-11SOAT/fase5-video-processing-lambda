"""
Repository Factory - Singleton factory for repository instances
This provides dependency injection and manages repository lifecycle
"""
from typing import Optional
from ..domain.repositories import IAuthRepository
from .cognito_repository import CognitoRepository

# Global singleton instance
_repository_instance: Optional[IAuthRepository] = None

def get_auth_repository() -> IAuthRepository:
    """
    Get or create singleton instance of the authentication repository
    
    Returns:
        IAuthRepository instance (CognitoRepository)
    """
    global _repository_instance
    if _repository_instance is None:
        _repository_instance = CognitoRepository()
    return _repository_instance

def reset_repository() -> None:
    """
    Reset the repository instance (useful for testing)
    """
    global _repository_instance
    _repository_instance = None
