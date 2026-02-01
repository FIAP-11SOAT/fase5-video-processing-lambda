from typing import Dict, Any

from src.auth_lambda.presentation.error_handler import handle_error
from src.auth_lambda.presentation.handlers import user_by_id_handler, user_info_handler, authenticate_handler, register_handler
from src.auth_lambda.presentation.request_parser import get_route_info
from src.auth_lambda.presentation.response_builder import create_error_response


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        path, http_method = get_route_info(event)

        if path == '/register' and http_method == 'POST':
            return register_handler(event, context)

        elif path == '/authenticate' and http_method == 'POST':
            return authenticate_handler(event, context)

        elif path == '/user-info' and http_method == 'GET':
            return user_info_handler(event, context)

        elif path.startswith('/user-by-id/') and http_method == 'GET':
            return user_by_id_handler(event, context)

        else:
            return create_error_response('Route not found', 404)

    except Exception as e:
        return handle_error(e)


main_handler = lambda_handler
