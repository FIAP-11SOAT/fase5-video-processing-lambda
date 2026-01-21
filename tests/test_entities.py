"""
Unit tests for domain entities
"""
import pytest
from datetime import datetime
from src.auth_lambda.domain.entities import User, AuthToken

class TestUser:
    """Test cases for User entity"""
    
    def test_user_creation(self):
        """Test user entity creation"""
        user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        
        assert user.user_id == "123"
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.enabled is True
    
    def test_user_to_dict(self):
        """Test user to dictionary conversion"""
        created_at = datetime(2024, 1, 1, 12, 0, 0)
        user = User(
            user_id="123",
            username="testuser",
            email="test@example.com",
            created_at=created_at,
            enabled=True
        )
        
        user_dict = user.to_dict()
        
        assert user_dict['user_id'] == "123"
        assert user_dict['username'] == "testuser"
        assert user_dict['email'] == "test@example.com"
        assert user_dict['created_at'] == created_at.isoformat()
        assert user_dict['enabled'] is True
    
    def test_user_to_dict_none_dates(self):
        """Test user to dict with None dates"""
        user = User(
            user_id="123",
            username="testuser"
        )
        
        user_dict = user.to_dict()
        
        assert user_dict['created_at'] is None
        assert user_dict['updated_at'] is None

class TestAuthToken:
    """Test cases for AuthToken entity"""
    
    def test_token_creation(self):
        """Test token entity creation"""
        token = AuthToken(
            access_token="access123",
            id_token="id123",
            refresh_token="refresh123"
        )
        
        assert token.access_token == "access123"
        assert token.id_token == "id123"
        assert token.refresh_token == "refresh123"
        assert token.token_type == "Bearer"
        assert token.expires_in == 3600
    
    def test_token_to_dict(self):
        """Test token to dictionary conversion"""
        token = AuthToken(
            access_token="access123",
            id_token="id123",
            refresh_token="refresh123",
            token_type="Bearer",
            expires_in=7200
        )
        
        token_dict = token.to_dict()
        
        assert token_dict['access_token'] == "access123"
        assert token_dict['id_token'] == "id123"
        assert token_dict['refresh_token'] == "refresh123"
        assert token_dict['token_type'] == "Bearer"
        assert token_dict['expires_in'] == 7200
