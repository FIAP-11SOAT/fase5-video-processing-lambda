from typing import Dict, Any

from src.auth_lambda.presentation.error_handler import handle_error
from src.auth_lambda.presentation.handlers import user_by_id_handler, user_info_handler, authenticate_handler, register_handler
from src.auth_lambda.presentation.request_parser import get_route_info
from src.auth_lambda.presentation.response_builder import create_error_response
from src.common.logging_config import get_logger, configure_logging


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    configure_logging()
    logger = get_logger(__name__)
    try:
        logger.info(f"Received event: ", extra={"event": event})

        path, http_method = get_route_info(event)

        logger.info(f"Route: {path}")
        logger.info(f"HTTP Method: {http_method}")

        # Remove o prefixo /auth se presente (vindo do API Gateway)
        if path.startswith('/auth'):
            path = path[5:]  # Remove '/auth'

        # Garante que o path comece com /
        if not path.startswith('/'):
            path = '/' + path

        if path == '/register' and http_method == 'POST':
            return register_handler(event, context)

        elif path == '/authenticate' and http_method == 'POST':
            return authenticate_handler(event, context)

        elif path == '/user-info' and http_method == 'GET':
            return user_info_handler(event, context)

        elif path.startswith('/user-by-id/') and http_method == 'GET':
            return user_by_id_handler(event, context)

        else:
            return create_error_response(f'Route not found: {http_method} {path}', 404)

    except Exception as e:
        return handle_error(e)


main_handler = lambda_handler
