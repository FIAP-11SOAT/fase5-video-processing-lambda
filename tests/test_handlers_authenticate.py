"""
Unit tests for authenticate handler
"""
import json
import pytest
from unittest.mock import Mock, patch

from src.auth_lambda.presentation.handlers import authenticate_handler
from src.auth_lambda.domain.entities import AuthToken
from src.auth_lambda.domain.exceptions import InvalidCredentialsException

class TestAuthenticateHandler:
    """Test cases for authenticate_handler"""
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_authenticate_handler_success(self, mock_get_repo):
        """Test successful authentication"""
        # Arrange
        mock_repo = Mock()
        mock_token = AuthToken(
            access_token="access123",
            id_token="id123",
            refresh_token="refresh123"
        )
        mock_repo.authenticate.return_value = mock_token
        mock_get_repo.return_value = mock_repo
        
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'SecurePass123!'
            })
        }
        
        # Act
        response = authenticate_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == 'Authentication successful'
        assert 'tokens' in body
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_authenticate_handler_invalid_credentials(self, mock_get_repo):
        """Test authentication with invalid credentials"""
        # Arrange
        mock_repo = Mock()
        mock_repo.authenticate.side_effect = InvalidCredentialsException("Invalid credentials")
        mock_get_repo.return_value = mock_repo
        
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': 'wrong'
            })
        }
        
        # Act
        response = authenticate_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 401
    
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_authenticate_handler_value_error(self, mock_get_repo):
        """Test authenticate handler with ValueError"""
        mock_repo = Mock()
        mock_repo.authenticate.side_effect = ValueError("Password required")
        mock_get_repo.return_value = mock_repo
        
        event = {
            'body': json.dumps({
                'username': 'testuser',
                'password': ''
            })
        }
        
        response = authenticate_handler(event, None)
        assert response['statusCode'] == 400
