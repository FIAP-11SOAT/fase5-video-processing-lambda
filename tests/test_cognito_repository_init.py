import pytest
import os
from src.auth_lambda.infrastructure.cognito_repository import CognitoRepository

class TestCognitoRepositoryInit:
    def setup_method(self):
        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'
        os.environ['COGNITO_USER_POOL_CLIENT_ID'] = 'test-client-id'

    def test_init_success(self):
        repo = CognitoRepository()
        assert repo.user_pool_id == 'us-east-1_test123'
        assert repo.client_id == 'test-client-id'

    def test_init_missing_env_vars(self):
        del os.environ['COGNITO_USER_POOL_ID']

        with pytest.raises(ValueError, match="COGNITO_USER_POOL_ID and COGNITO_USER_POOL_CLIENT_ID must be set"):
            CognitoRepository()

        os.environ['COGNITO_USER_POOL_ID'] = 'us-east-1_test123'