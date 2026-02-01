from typing import Dict, Any

from src.auth_lambda.application.authenticate_user_use_case import AuthenticateUserUseCase
from src.auth_lambda.application.get_user_by_id_use_case import GetUserByIdUseCase
from src.auth_lambda.application.get_user_info_use_case import GetUserInfoUseCase
from src.auth_lambda.application.register_user_use_case import RegisterUserUseCase
from src.auth_lambda.infrastructure.repository_factory import get_auth_repository
from src.auth_lambda.presentation.error_handler import handle_error
from src.auth_lambda.presentation.request_parser import parse_body, extract_bearer_token, extract_path_parameter
from src.auth_lambda.presentation.response_builder import create_success_response
from src.common.logging_config import get_logger

logger = get_logger(__name__)


def register_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Parse request
        body = parse_body(event)
        username = body.get('username')
        password = body.get('password')
        email = body.get('email')

        logger.info("register_user_request", username=username, email=email)

        # Execute use case
        repository = get_auth_repository()
        use_case = RegisterUserUseCase(repository)
        user = use_case.execute(username, password, email)

        logger.info("user_registered_successfully", user_id=user.user_id, username=username)

        # Build response
        return create_success_response({
            'message': 'User registered successfully',
            'user': user.to_dict()
        }, status_code=201)

    except Exception as e:
        return handle_error(e)


def authenticate_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Parse request
        body = parse_body(event)
        username = body.get('username')
        password = body.get('password')

        logger.info("authenticate_user_request", username=username)

        # Execute use case
        repository = get_auth_repository()
        use_case = AuthenticateUserUseCase(repository)
        token = use_case.execute(username, password)

        logger.info("user_authenticated_successfully", username=username)

        # Build response
        return create_success_response({
            'message': 'Authentication successful',
            'tokens': token.to_dict()
        })

    except Exception as e:
        return handle_error(e)


def user_info_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Parse request
        access_token = extract_bearer_token(event)

        logger.info("get_user_info_request")

        # Execute use case
        repository = get_auth_repository()
        use_case = GetUserInfoUseCase(repository)
        user = use_case.execute(access_token)

        logger.info("user_info_retrieved", user_id=user.user_id, username=user.username)

        # Build response
        return create_success_response({
            'user': user.to_dict()
        })

    except Exception as e:
        return handle_error(e)


def user_by_id_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        user_id = extract_path_parameter(event, 'user_id')

        logger.info("get_user_by_id_request", user_id=user_id)

        # Execute use case
        repository = get_auth_repository()
        use_case = GetUserByIdUseCase(repository)
        user = use_case.execute(user_id)

        logger.info("user_retrieved_by_id", user_id=user.user_id, username=user.username)

        # Build response
        return create_success_response({
            'user': user.to_dict()
        })

    except Exception as e:
        return handle_error(e)
