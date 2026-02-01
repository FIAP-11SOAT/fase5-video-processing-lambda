import pytest
from unittest.mock import Mock
from src.auth_lambda.application.use_cases import (
    RegisterUserUseCase,
    AuthenticateUserUseCase,
    GetUserInfoUseCase,
    GetUserByIdUseCase,
)
from src.auth_lambda.domain.entities import User, AuthToken
import os
from base64 import b64encode

class TestRegisterUserUseCase:
    def test_register_user_success(self):
        mock_repository = Mock()
        expected_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repository.register_user.return_value = expected_user

        use_case = RegisterUserUseCase(mock_repository)

        result = use_case.execute("testuser", "SecurePass123!", "test@example.com")

        assert result == expected_user
        mock_repository.register_user.assert_called_once_with(
            "testuser", "SecurePass123!", "test@example.com"
        )

    def test_register_user_short_username(self):
        mock_repository = Mock()
        use_case = RegisterUserUseCase(mock_repository)

        with pytest.raises(ValueError, match="Username must be at least 3 characters"):
            use_case.execute("ab", "SecurePass123!")

    def test_register_user_short_password(self):
        mock_repository = Mock()
        use_case = RegisterUserUseCase(mock_repository)

        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            use_case.execute("testuser", "short")

class TestAuthenticateUserUseCase:
    def test_authenticate_success(self):
        mock_repository = Mock()
        expected_token = AuthToken(
            access_token="access123",
            id_token="id123",
            refresh_token="refresh123"
        )
        mock_repository.authenticate.return_value = expected_token

        use_case = AuthenticateUserUseCase(mock_repository)

        result = use_case.execute("testuser", "SecurePass123!")

        assert result == expected_token
        mock_repository.authenticate.assert_called_once_with("testuser", "SecurePass123!")

    def test_authenticate_missing_credentials(self):
        mock_repository = Mock()
        use_case = AuthenticateUserUseCase(mock_repository)

        with pytest.raises(ValueError, match="Username and password are required"):
            use_case.execute("", "password")

class TestGetUserInfoUseCase:
    def test_get_user_info_success(self):
        mock_repository = Mock()
        expected_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repository.get_user_info.return_value = expected_user

        use_case = GetUserInfoUseCase(mock_repository)

        
        token = "header.payload.signature"

        result = use_case.execute(token)

        assert result == expected_user
        mock_repository.get_user_info.assert_called_once_with(token)

    def test_get_user_info_missing_token(self):
        mock_repository = Mock()
        use_case = GetUserInfoUseCase(mock_repository)

        with pytest.raises(ValueError, match="Access token is required"):
            use_case.execute("")

class TestGetUserByIdUseCase:
    def test_get_user_by_id_success(self):
        mock_repository = Mock()
        expected_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repository.get_user_by_id.return_value = expected_user

        use_case = GetUserByIdUseCase(mock_repository)

        # create valid ms_token (base64 of pool_id:client_id)
        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
        ms_token = b64encode(f"{os.environ['COGNITO_USER_POOL_ID']}:{os.environ['COGNITO_CLIENT_ID']}".encode()).decode()

        result = use_case.execute(ms_token, "123")

        assert result == expected_user
        mock_repository.get_user_by_id.assert_called_once_with("123")

    def test_get_user_by_id_missing_id(self):
        mock_repository = Mock()
        use_case = GetUserByIdUseCase(mock_repository)

        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
        ms_token = b64encode(f"{os.environ['COGNITO_USER_POOL_ID']}:{os.environ['COGNITO_CLIENT_ID']}".encode()).decode()

        with pytest.raises(ValueError, match="User ID is required"):
            use_case.execute(ms_token, "")
