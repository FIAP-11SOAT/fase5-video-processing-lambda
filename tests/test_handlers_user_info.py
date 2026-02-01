import json
import pytest
from unittest.mock import Mock, patch
import os
from base64 import b64encode

from src.auth_lambda.presentation.handlers import user_info_handler, user_by_id_handler
from src.auth_lambda.domain.entities import User
from src.auth_lambda.domain.exceptions import InvalidTokenException, UserNotFoundException

class TestUserInfoHandler:
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_success(self, mock_get_repo):
        mock_repo = Mock()
        mock_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repo.get_user_info.return_value = mock_user
        mock_get_repo.return_value = mock_repo

        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
        token = "header.payload.signature"
        event = {
            'headers': {
                'Authorization': f'Bearer {token}'
            }
        }

        response = user_info_handler(event, None)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['user']['username'] == 'testuser'

    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_missing_header(self, mock_get_repo):
        event = {'headers': {}}
        response = user_info_handler(event, None)
        assert response['statusCode'] == 400

    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_invalid_token(self, mock_get_repo):
        mock_repo = Mock()
        mock_repo.get_user_info.side_effect = InvalidTokenException("Invalid token")
        mock_get_repo.return_value = mock_repo

        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
        token = "header.payload.signature"
        event = {'headers': {'Authorization': f'Bearer {token}'}}

        response = user_info_handler(event, None)
        assert response['statusCode'] == 404

    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_info_handler_lowercase_auth_header(self, mock_get_repo):
        mock_repo = Mock()
        mock_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repo.get_user_info.return_value = mock_user
        mock_get_repo.return_value = mock_repo

        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
        token = "header.payload.signature"
        event = {'headers': {'authorization': f'Bearer {token}'}}

        response = user_info_handler(event, None)
        assert response['statusCode'] == 200

class TestUserByIdHandler:
    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_by_id_handler_success(self, mock_get_repo):
        mock_repo = Mock()
        mock_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repo.get_user_by_id.return_value = mock_user
        mock_get_repo.return_value = mock_repo

        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
        token = b64encode(f"{os.environ['COGNITO_USER_POOL_ID']}:{os.environ['COGNITO_CLIENT_ID']}".encode()).decode()
        event = {
            'headers': {'X-MS-Token': token},
            'pathParameters': {'user_id': '123'}
        }

        response = user_by_id_handler(event, None)

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['user']['user_id'] == '123'

    @patch('src.auth_lambda.presentation.handlers.get_auth_repository')
    def test_user_by_id_handler_not_found(self, mock_get_repo):
        mock_repo = Mock()
        mock_repo.get_user_by_id.side_effect = UserNotFoundException("User not found")
        mock_get_repo.return_value = mock_repo

        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
        token = b64encode(f"{os.environ['COGNITO_USER_POOL_ID']}:{os.environ['COGNITO_CLIENT_ID']}".encode()).decode()
        event = {
            'headers': {'X-MS-Token': token},
            'pathParameters': {'user_id': '999'}
        }

        response = user_by_id_handler(event, None)
        assert response['statusCode'] == 404