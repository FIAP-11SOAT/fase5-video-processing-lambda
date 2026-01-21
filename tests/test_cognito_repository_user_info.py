"""
Unit tests for CognitoRepository user info operations
"""
import pytest
import os
from unittest.mock import patch, Mock
from datetime import datetime
from botocore.exceptions import ClientError

from src.auth_lambda.infrastructure.cognito_repository import CognitoRepository
from src.auth_lambda.domain.exceptions import (
    InvalidTokenException,
    UserNotFoundException,
    AuthenticationException
)

class TestCognitoRepositoryUserInfo:
    """Test cases for CognitoRepository user info operations"""
    
    def setup_method(self):
        """Setup test fixtures"""
        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
    
    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_get_user_info_success(self, mock_boto3):
        """Test successful get user info"""
        # Arrange
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        mock_client.get_user.return_value = {
            'Username': 'testuser',
            'UserAttributes': [
                {'Name': 'sub', 'Value': 'user-123'},
                {'Name': 'email', 'Value': 'test@example.com'}
            ],
            'UserCreateDate': datetime(2024, 1, 1),
            'UserLastModifiedDate': datetime(2024, 1, 2)
        }
        
        repo = CognitoRepository()
        
        # Act
        user = repo.get_user_info('valid-token')
        
        # Assert
        assert user.user_id == 'user-123'
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        mock_client.get_user.assert_called_once_with(AccessToken='valid-token')
    
    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_get_user_info_invalid_token(self, mock_boto3):
        """Test get user info with invalid token"""
        # Arrange
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        error_response = {'Error': {'Code': 'NotAuthorizedException', 'Message': 'Invalid token'}}
        mock_client.get_user.side_effect = ClientError(error_response, 'GetUser')
        
        repo = CognitoRepository()
        
        # Act & Assert
        with pytest.raises(InvalidTokenException):
            repo.get_user_info('invalid-token')
    
    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_get_user_info_other_error(self, mock_boto3):
        """Test get user info with other error"""
        # Arrange
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        error_response = {'Error': {'Code': 'InternalError', 'Message': 'Internal error'}}
        mock_client.get_user.side_effect = ClientError(error_response, 'GetUser')
        
        repo = CognitoRepository()
        
        # Act & Assert
        with pytest.raises(AuthenticationException):
            repo.get_user_info('valid-token')
    
    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_get_user_by_id_success(self, mock_boto3):
        """Test successful get user by ID"""
        # Arrange
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        mock_client.list_users.return_value = {
            'Users': [
                {
                    'Username': 'testuser',
                    'Attributes': [
                        {'Name': 'email', 'Value': 'test@example.com'}
                    ],
                    'UserCreateDate': datetime(2024, 1, 1),
                    'UserLastModifiedDate': datetime(2024, 1, 2),
                    'Enabled': True
                }
            ]
        }
        
        repo = CognitoRepository()
        
        # Act
        user = repo.get_user_by_id('user-123')
        
        # Assert
        assert user.user_id == 'user-123'
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.enabled is True
        mock_client.list_users.assert_called_once()
    
    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_get_user_by_id_not_found(self, mock_boto3):
        """Test get user by ID when user not found"""
        # Arrange
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        mock_client.list_users.return_value = {'Users': []}
        
        repo = CognitoRepository()
        
        # Act & Assert
        with pytest.raises(UserNotFoundException):
            repo.get_user_by_id('nonexistent-id')
    
    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_get_user_by_id_error(self, mock_boto3):
        """Test get user by ID with error"""
        # Arrange
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        
        error_response = {'Error': {'Code': 'InternalError', 'Message': 'Internal error'}}
        mock_client.list_users.side_effect = ClientError(error_response, 'ListUsers')
        
        repo = CognitoRepository()
        
        # Act & Assert
        with pytest.raises(AuthenticationException):
            repo.get_user_by_id('user-123')
