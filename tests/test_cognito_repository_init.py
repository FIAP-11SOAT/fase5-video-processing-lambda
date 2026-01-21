"""
Unit tests for CognitoRepository initialization
"""
import pytest
import os
from src.auth_lambda.infrastructure.cognito_repository import CognitoRepository

class TestCognitoRepositoryInit:
    """Test cases for CognitoRepository initialization"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Set environment variables
        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_CLIENT_ID'] = 'test-client-id'
    
    def test_init_success(self):
        """Test successful initialization"""
        repo = CognitoRepository()
        assert repo.user_pool_id == 'us-east-1_test123'
        assert repo.client_id == 'test-client-id'
    
    def test_init_missing_env_vars(self):
        """Test initialization with missing environment variables"""
        del os.environ['COGNITO_USER_POOL_ID']
        
        with pytest.raises(ValueError, match="COGNITO_USER_POOL_ID and COGNITO_CLIENT_ID must be set"):
            CognitoRepository()
        
        # Restore env var
        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
