import pytest
import os
from unittest.mock import patch, Mock
from botocore.exceptions import ClientError

from src.auth_lambda.infrastructure.cognito_repository import CognitoRepository
from src.auth_lambda.domain.exceptions import (
    UserAlreadyExistsException,
    AuthenticationException,
)

class TestCognitoRepositoryRegister:
    def setup_method(self):
        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_register_user_success(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        mock_client.sign_up.return_value = {'UserSub': 'user-123'}

        repo = CognitoRepository()

        user = repo.register_user('testuser', 'Password123!', 'test@example.com')

        assert user.user_id == 'user-123'
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.enabled is True
        mock_client.sign_up.assert_called_once()

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_register_user_already_exists(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client

        error_response = {'Error': {'Code': 'UsernameExistsException', 'Message': 'User exists'}}
        mock_client.sign_up.side_effect = ClientError(error_response, 'SignUp')

        repo = CognitoRepository()

        with pytest.raises(UserAlreadyExistsException):
            repo.register_user('existinguser', 'Password123!')

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_register_user_invalid_password(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client

        error_response = {'Error': {'Code': 'InvalidPasswordException', 'Message': 'Password too weak'}}
        mock_client.sign_up.side_effect = ClientError(error_response, 'SignUp')

        repo = CognitoRepository()

        with pytest.raises(ValueError):
            repo.register_user('testuser', 'weak')

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_register_user_other_error(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client

        error_response = {'Error': {'Code': 'InternalError', 'Message': 'Internal error'}}
        mock_client.sign_up.side_effect = ClientError(error_response, 'SignUp')

        repo = CognitoRepository()

        with pytest.raises(AuthenticationException):
            repo.register_user('testuser', 'Password123!')