import os
from datetime import datetime
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from src.auth_lambda.domain.entities import User, AuthToken
from src.auth_lambda.domain.exceptions import UserAlreadyExistsException, AuthenticationException, \
    InvalidCredentialsException, InvalidTokenException, UserNotFoundException
from src.auth_lambda.domain.repositories import IAuthRepository
from src.common.logging_config import get_logger

logger = get_logger(__name__)


class CognitoRepository(IAuthRepository):

    def __init__(self, user_pool_id: Optional[str] = None, client_id: Optional[str] = None):
        self.user_pool_id = user_pool_id or os.environ.get('COGNITO_USER_POOL_ID')
        self.client_id = client_id or os.environ.get('COGNITO_USER_POOL_CLIENT_ID')

        if not self.user_pool_id or not self.client_id:
            raise ValueError("COGNITO_USER_POOL_ID and COGNITO_USER_POOL_CLIENT_ID must be set")

        self.cognito_client = boto3.client('cognito-idp')

    def register_user(self, username: str, password: str, email: Optional[str] = None) -> User:
        try:
            user_attributes = []
            if email:
                user_attributes.append({
                    'Name': 'email',
                    'Value': email
                })

            response = self.cognito_client.sign_up(
                ClientId=self.client_id,
                Username=username,
                Password=password,
                UserAttributes=user_attributes
            )

            self.cognito_client.admin_confirm_sign_up(
                UserPoolId=self.user_pool_id,
                Username=username
            )

            return User(
                user_id=response['UserSub'],
                username=username,
                email=email,
                created_at=datetime.now(),
                enabled=True
            )

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'UsernameExistsException':
                raise UserAlreadyExistsException(f"User {username} already exists")
            elif error_code == 'InvalidPasswordException':
                raise ValueError(e.response['Error']['Message'])
            else:
                raise AuthenticationException(f"Registration failed: {e.response['Error']['Message']}")

    def authenticate(self, username: str, password: str) -> AuthToken:
        try:
            response = self.cognito_client.initiate_auth(
                ClientId=self.client_id,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': username,
                    'PASSWORD': password
                }
            )

            auth_result = response['AuthenticationResult']

            return AuthToken(
                access_token=auth_result['AccessToken'],
                id_token=auth_result['IdToken'],
                refresh_token=auth_result.get('RefreshToken', ''),
                token_type='Bearer',
                expires_in=auth_result.get('ExpiresIn', 3600)
            )

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code in ['NotAuthorizedException', 'UserNotFoundException']:
                logger.error(
                    f"Authentication failed for user {username}: {e.response['Error']['Message']} : Code {error_code}")
                raise InvalidCredentialsException("Invalid username or password")
            else:
                raise AuthenticationException(f"Authentication failed: {e.response['Error']['Message']}")

    def get_user_info(self, access_token: str) -> User:
        try:
            response = self.cognito_client.get_user(
                AccessToken=access_token
            )

            username = response['Username']
            email = None
            user_id = None

            for attr in response.get('UserAttributes', []):
                if attr['Name'] == 'email':
                    email = attr['Value']
                elif attr['Name'] == 'sub':
                    user_id = attr['Value']

            return User(
                user_id=user_id,
                username=username,
                email=email,
                created_at=response.get('UserCreateDate'),
                updated_at=response.get('UserLastModifiedDate'),
                enabled=True
            )

        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NotAuthorizedException':
                raise InvalidTokenException("Invalid or expired token")
            else:
                raise AuthenticationException(f"Failed to get user info: {e.response['Error']['Message']}")

    def get_user_by_id(self, user_id: str) -> User:
        try:
            response = self.cognito_client.list_users(
                UserPoolId=self.user_pool_id,
                Filter=f'sub = "{user_id}"'
            )

            if not response.get('Users'):
                raise UserNotFoundException(f"User with ID {user_id} not found")

            user_data = response['Users'][0]
            username = user_data['Username']
            email = None

            for attr in user_data.get('Attributes', []):
                if attr['Name'] == 'email':
                    email = attr['Value']

            user = User(user_id=user_id, username=username, email=email,
                             created_at=user_data.get('UserCreateDate'),
                             updated_at=user_data.get('UserLastModifiedDate'), enabled=user_data.get('Enabled', True))
            return user

        except ClientError as e:
            raise AuthenticationException(f"Failed to get user: {e.response['Error']['Message']}")
