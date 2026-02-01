from typing import Dict, Any
import os
from base64 import b64encode

from src.auth_lambda.application.authenticate_user_use_case import AuthenticateUserUseCase
from src.auth_lambda.application.get_user_by_id_use_case import GetUserByIdUseCase
from src.auth_lambda.application.get_user_info_use_case import GetUserInfoUseCase
from src.auth_lambda.application.register_user_use_case import RegisterUserUseCase
from src.auth_lambda.infrastructure.repository_factory import get_auth_repository
from src.auth_lambda.presentation.error_handler import handle_error
from src.auth_lambda.presentation.request_parser import (
    parse_body,
    extract_bearer_token,
    extract_path_parameter,
    extract_ms_token,
)
from src.auth_lambda.presentation.response_builder import create_success_response
from src.auth_lambda.domain.exceptions import InvalidTokenException
from src.common.logging_config import get_logger

logger = get_logger(__name__)


def register_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        body = parse_body(event)
        username = body.get("username")
        password = body.get("password")
        email = body.get("email")

        logger.info("register_user_request", username=username, email=email)

        repository = get_auth_repository()
        use_case = RegisterUserUseCase(repository)
        user = use_case.execute(username, password, email)

        logger.info("user_registered_successfully", user_id=user.user_id, username=username)

        return create_success_response(
            {"message": "User registered successfully", "user": user.to_dict()}, status_code=201
        )

    except Exception as e:
        return handle_error(e)


def authenticate_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        body = parse_body(event)
        username = body.get("username")
        password = body.get("password")

        logger.info("authenticate_user_request", username=username)

        repository = get_auth_repository()
        use_case = AuthenticateUserUseCase(repository)
        token = use_case.execute(username, password)

        logger.info("user_authenticated_successfully", username=username)

        return create_success_response({"message": "Authentication successful", "tokens": token.to_dict()})

    except Exception as e:
        return handle_error(e)


def user_info_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        access_token = extract_bearer_token(event)

        logger.info("get_user_info_request")

        repository = get_auth_repository()
        use_case = GetUserInfoUseCase(repository)
        user = use_case.execute(access_token)

        logger.info("user_info_retrieved", user_id=user.user_id, username=user.username)

        return create_success_response({"user": user.to_dict()})

    except Exception as e:
        return handle_error(e)


def user_by_id_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        ms_token = extract_ms_token(event)

        user_pool_id = os.environ.get("COGNITO_USER_POOL_ID")
        client_id = os.environ.get("COGNITO_CLIENT_ID")
        if not user_pool_id or not client_id:
            raise ValueError("COGNITO_USER_POOL_ID and COGNITO_CLIENT_ID must be set for MS token validation")

        expected = b64encode(f"{user_pool_id}:{client_id}".encode()).decode()
        if ms_token != expected:
            raise InvalidTokenException("Invalid MS token")

        user_id = extract_path_parameter(event, "user_id")

        logger.info("get_user_by_id_request", user_id=user_id)

        repository = get_auth_repository()
        use_case = GetUserByIdUseCase(repository)
        user = use_case.execute(user_id)

        logger.info("user_retrieved_by_id", user_id=user.user_id, username=user.username)

        return create_success_response({"user": user.to_dict()})

    except Exception as e:
        return handle_error(e)