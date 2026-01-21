"""
Unit tests for authentication use cases
"""
import pytest
from unittest.mock import Mock
from src.auth_lambda.application.use_cases import (
    RegisterUserUseCase,
    AuthenticateUserUseCase,
    GetUserInfoUseCase,
    GetUserByIdUseCase
)
from src.auth_lambda.domain.entities import User, AuthToken
from src.auth_lambda.domain.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException
)

class TestRegisterUserUseCase:
    """Test cases for RegisterUserUseCase"""
    
    def test_register_user_success(self):
        """Test successful user registration"""
        # Arrange
        mock_repository = Mock()
        expected_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repository.register_user.return_value = expected_user
        
        use_case = RegisterUserUseCase(mock_repository)
        
        # Act
        result = use_case.execute("testuser", "SecurePass123!", "test@example.com")
        
        # Assert
        assert result == expected_user
        mock_repository.register_user.assert_called_once_with(
            "testuser", "SecurePass123!", "test@example.com"
        )
    
    def test_register_user_short_username(self):
        """Test registration with short username"""
        mock_repository = Mock()
        use_case = RegisterUserUseCase(mock_repository)
        
        with pytest.raises(ValueError, match="Username must be at least 3 characters"):
            use_case.execute("ab", "SecurePass123!")
    
    def test_register_user_short_password(self):
        """Test registration with short password"""
        mock_repository = Mock()
        use_case = RegisterUserUseCase(mock_repository)
        
        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            use_case.execute("testuser", "short")

class TestAuthenticateUserUseCase:
    """Test cases for AuthenticateUserUseCase"""
    
    def test_authenticate_success(self):
        """Test successful authentication"""
        # Arrange
        mock_repository = Mock()
        expected_token = AuthToken(
            access_token="access123",
            id_token="id123",
            refresh_token="refresh123"
        )
        mock_repository.authenticate.return_value = expected_token
        
        use_case = AuthenticateUserUseCase(mock_repository)
        
        # Act
        result = use_case.execute("testuser", "SecurePass123!")
        
        # Assert
        assert result == expected_token
        mock_repository.authenticate.assert_called_once_with("testuser", "SecurePass123!")
    
    def test_authenticate_missing_credentials(self):
        """Test authentication with missing credentials"""
        mock_repository = Mock()
        use_case = AuthenticateUserUseCase(mock_repository)
        
        with pytest.raises(ValueError, match="Username and password are required"):
            use_case.execute("", "password")

class TestGetUserInfoUseCase:
    """Test cases for GetUserInfoUseCase"""
    
    def test_get_user_info_success(self):
        """Test successful retrieval of user info"""
        # Arrange
        mock_repository = Mock()
        expected_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repository.get_user_info.return_value = expected_user
        
        use_case = GetUserInfoUseCase(mock_repository)
        
        # Act
        result = use_case.execute("valid_token")
        
        # Assert
        assert result == expected_user
        mock_repository.get_user_info.assert_called_once_with("valid_token")
    
    def test_get_user_info_missing_token(self):
        """Test getting user info with missing token"""
        mock_repository = Mock()
        use_case = GetUserInfoUseCase(mock_repository)
        
        with pytest.raises(ValueError, match="Access token is required"):
            use_case.execute("")

class TestGetUserByIdUseCase:
    """Test cases for GetUserByIdUseCase"""
    
    def test_get_user_by_id_success(self):
        """Test successful retrieval of user by ID"""
        # Arrange
        mock_repository = Mock()
        expected_user = User(
            user_id="123",
            username="testuser",
            email="test@example.com"
        )
        mock_repository.get_user_by_id.return_value = expected_user
        
        use_case = GetUserByIdUseCase(mock_repository)
        
        # Act
        result = use_case.execute("123")
        
        # Assert
        assert result == expected_user
        mock_repository.get_user_by_id.assert_called_once_with("123")
    
    def test_get_user_by_id_missing_id(self):
        """Test getting user with missing ID"""
        mock_repository = Mock()
        use_case = GetUserByIdUseCase(mock_repository)
        
        with pytest.raises(ValueError, match="User ID is required"):
            use_case.execute("")
