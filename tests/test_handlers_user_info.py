"""
Unit tests for user info handlers
"""
import json
import pytest
from unittest.mock import Mock, patch

from src.auth_lambda.presentation.handlers import user_info_handler, user_by_id_handler
from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.exceptions import InvalidTokenException, UserNotFoundException

class TestUserInfoHandler:
    """Test cases for user_info_handler"""
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_success(self, mock_get_repo):
        """Test successful user info retrieval"""
        # Arrange
        mock_repo = Mock()
        mock_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repo.get_user_info.return_value = mock_user
        mock_get_repo.return_value = mock_repo
        
        event = {
            'headers': {
                'Authorization': 'Bearer valid_token'
            }
        }
        
        # Act
        response = user_info_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['user']['username'] == 'testuser'
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_missing_header(self, mock_get_repo):
        """Test user info with missing authorization header"""
        event = {
            'headers': {}
        }
        
        # Act
        response = user_info_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 400
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_invalid_token(self, mock_get_repo):
        """Test user info with invalid token"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_user_info.side_effect = InvalidTokenException("Invalid token")
        mock_get_repo.return_value = mock_repo
        
        event = {
            'headers': {
                'Authorization': 'Bearer invalid_token'
            }
        }
        
        # Act
        response = user_info_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 404
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_lowercase_auth_header(self, mock_get_repo):
        """Test user info handler with lowercase authorization header"""
        mock_repo = Mock()
        mock_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repo.get_user_info.return_value = mock_user
        mock_get_repo.return_value = mock_repo
        
        event = {
            'headers': {
                'authorization': 'Bearer valid_token'  # lowercase
            }
        }
        
        response = user_info_handler(event, None)
        assert response['statusCode'] == 200

class TestUserByIdHandler:
    """Test cases for user_by_id_handler"""
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_by_id_handler_success(self, mock_get_repo):
        """Test successful user retrieval by ID"""
        # Arrange
        mock_repo = Mock()
        mock_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repo.get_user_by_id.return_value = mock_user
        mock_get_repo.return_value = mock_repo
        
        event = {
            'pathParameters': {
                'user_id': '123'
            }
        }
        
        # Act
        response = user_by_id_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['user']['user_id'] == '123'
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_by_id_handler_not_found(self, mock_get_repo):
        """Test user by ID not found"""
        # Arrange
        mock_repo = Mock()
        mock_repo.get_user_by_id.side_effect = UserNotFoundException("User not found")
        mock_get_repo.return_value = mock_repo
        
        event = {
            'pathParameters': {
                'user_id': '999'
            }
        }
        
        # Act
        response = user_by_id_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 404
