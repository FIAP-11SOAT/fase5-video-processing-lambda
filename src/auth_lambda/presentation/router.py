"""
Router - Routes API Gateway requests to appropriate handlers
This is the main Lambda entry point that delegates to specific handlers
"""
from typing import Dict, Any

from .handlers import (
    register_handler,
    authenticate_handler,
    user_info_handler,
    user_by_id_handler
)
from .response_builder import create_error_response
from .error_handler import handle_error
from .request_parser import get_route_info

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler - routes requests to appropriate handler
    This is the entry point for AWS Lambda
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    try:
        # Extract route information
        path, http_method = get_route_info(event)
        
        # Route to appropriate handler based on path and method
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

# Alias for backward compatibility
main_handler = lambda_handler
