import json
import pytest

from src.auth_lambda.presentation.response_builder import create_response
from src.auth_lambda.presentation.error_handler import handle_error
from src.auth_lambda.domain.exceptions import DomainException

class TestHandlerUtils:
    def test_create_response(self):
        response = create_response(200, {'message': 'success'})

        assert response['statusCode'] == 200
        assert 'headers' in response
        assert response['headers']['Content-Type'] == 'application/json'
        body = json.loads(response['body'])
        assert body['message'] == 'success'

    def test_handle_error_value_error(self):
        error = ValueError("Invalid input")
        response = handle_error(error)
        assert response['statusCode'] == 400

    def test_handle_error_domain_exception(self):
        error = DomainException("Domain error")
        response = handle_error(error)
        assert response['statusCode'] == 400

    def test_handle_error_generic(self):
        error = Exception("Something went wrong")
        response = handle_error(error)
        assert response['statusCode'] == 500