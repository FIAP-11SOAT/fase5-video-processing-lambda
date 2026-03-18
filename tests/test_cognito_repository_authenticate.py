import pytest
import os
from unittest.mock import patch, Mock
from botocore.exceptions import ClientError

from src.auth_lambda.infrastructure.cognito_repository import CognitoRepository
from src.auth_lambda.domain.exceptions import (
    InvalidCredentialsException,
    AuthenticationException,
)

class TestCognitoRepositoryAuthenticate:
    def setup_method(self):
        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_USER_POOL_CLIENT_ID'] = 'test-client-id'

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_authenticate_success(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        mock_client.initiate_auth.return_value = {
            'AuthenticationResult': {
                'AccessToken': 'access-token',
                'IdToken': 'id-token',
                'RefreshToken': 'refresh-token',
                'ExpiresIn': 3600
            }
        }

        repo = CognitoRepository()

        token = repo.authenticate('testuser', 'Password123!')

        assert token.access_token == 'access-token'
        assert token.id_token == 'id-token'
        assert token.refresh_token == 'refresh-token'
        assert token.expires_in == 3600
        mock_client.initiate_auth.assert_called_once()

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_authenticate_invalid_credentials(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client

        error_response = {'Error': {'Code': 'NotAuthorizedException', 'Message': 'Invalid'}}
        mock_client.initiate_auth.side_effect = ClientError(error_response, 'InitiateAuth')

        repo = CognitoRepository()

        with pytest.raises(InvalidCredentialsException):
            repo.authenticate('testuser', 'WrongPassword')

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_authenticate_user_not_found(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client

        error_response = {'Error': {'Code': 'UserNotFoundException', 'Message': 'User not found'}}
        mock_client.initiate_auth.side_effect = ClientError(error_response, 'InitiateAuth')

        repo = CognitoRepository()

        with pytest.raises(InvalidCredentialsException):
            repo.authenticate('nonexistent', 'Password123!')

    @patch('src.auth_lambda.infrastructure.cognito_repository.boto3')
    def test_authenticate_other_error(self, mock_boto3):
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client

        error_response = {'Error': {'Code': 'InternalError', 'Message': 'Internal error'}}
        mock_client.initiate_auth.side_effect = ClientError(error_response, 'InitiateAuth')

        repo = CognitoRepository()

        with pytest.raises(AuthenticationException):
            repo.authenticate('testuser', 'Password123!')