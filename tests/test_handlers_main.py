import pytest
from unittest.mock import patch

from src.auth_lambda.presentation.router import main_handler

class TestMainHandler:
    def test_main_handler_register_route(self):
        with patch('src.auth_lambda.presentation.router.register_handler') as mock_register:
            mock_register.return_value = {'statusCode': 201}

            event = {
                'path': '/register',
                'httpMethod': 'POST'
            }

            response = main_handler(event, None)
            assert response['statusCode'] == 201
            mock_register.assert_called_once()

    def test_main_handler_authenticate_route(self):
        with patch('src.auth_lambda.presentation.router.authenticate_handler') as mock_auth:
            mock_auth.return_value = {'statusCode': 200}

            event = {
                'path': '/authenticate',
                'httpMethod': 'POST'
            }

            response = main_handler(event, None)
            assert response['statusCode'] == 200
            mock_auth.assert_called_once()

    def test_main_handler_user_info_route(self):
        with patch('src.auth_lambda.presentation.router.user_info_handler') as mock_info:
            mock_info.return_value = {'statusCode': 200}

            event = {
                'path': '/user-info',
                'httpMethod': 'GET'
            }

            response = main_handler(event, None)
            assert response['statusCode'] == 200
            mock_info.assert_called_once()

    def test_main_handler_user_by_id_route(self):
        with patch('src.auth_lambda.presentation.router.user_by_id_handler') as mock_by_id:
            mock_by_id.return_value = {'statusCode': 200}

            event = {
                'path': '/user-by-id/123',
                'httpMethod': 'GET'
            }

            response = main_handler(event, None)
            assert response['statusCode'] == 200
            mock_by_id.assert_called_once()

    def test_main_handler_not_found(self):
        event = {
            'path': '/unknown',
            'httpMethod': 'GET'
        }

        response = main_handler(event, None)
        assert response['statusCode'] == 404

    def test_main_handler_exception(self):
        event = None  # This will cause an error

        response = main_handler(event, None)
        assert response['statusCode'] == 500