"""
Unit tests for register handler
"""
import json
import pytest
from unittest.mock import Mock, patch

from src.auth_lambda.presentation.handlers import register_handler
from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.exceptions import UserAlreadyExistsException


class TestRegisterHandler:
    """Test cases for register_handler"""
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_register_handler_success(self, mock_get_repo):
        """Test successful user registration"""
        # Arrange
        mock_repo = Mock()
        mock_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repo.register_user.return_value = mock_user
        mock_get_repo.return_value = mock_repo
        
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'SecurePass123!',
                'email': 'test@example.com'
            })
        }
        
        # Act
        response = register_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['message'] == 'User registered successfully'
        assert body['user']['username'] == 'testuser'
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_register_handler_user_exists(self, mock_get_repo):
        """Test registration with existing user"""
        # Arrange
        mock_repo = Mock()
        mock_repo.register_user.side_effect = UserAlreadyExistsException("User exists")
        mock_get_repo.return_value = mock_repo
        
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'SecurePass123!'
            })
        }
        
        # Act
        response = register_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 409
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_register_handler_value_error(self, mock_get_repo):
        """Test register handler with ValueError from use case"""
        mock_repo = Mock()
        mock_repo.register_user.side_effect = ValueError("Username too short")
        mock_get_repo.return_value = mock_repo
        
        event = {
            'body': json.dumps({
                'username': 'ab',
                'password': 'Password123!'
            })
        }
        
        response = register_handler(event, None)
        assert response['statusCode'] == 400
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_register_handler_generic_exception(self, mock_get_repo):
        """Test register handler with generic exception"""
        mock_repo = Mock()
        mock_repo.register_user.side_effect = Exception("Unexpected error")
        mock_get_repo.return_value = mock_repo
        
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'Password123!'
            })
        }
        
        response = register_handler(event, None)
        assert response['statusCode'] == 500
