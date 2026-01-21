"""
Error Handler - Centralized error handling for API responses
Converts exceptions to appropriate HTTP responses
"""
from typing import Dict, Any
import json

from src.common.logging_config import get_logger
from ..domain.exceptions import (
    DomainException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFoundException,
    InvalidTokenException,
    AuthenticationException
)
from .response_builder import create_error_response

logger = get_logger(__name__)

def handle_error(error: Exception) -> Dict[str, Any]:
    """
    Handle errors and return appropriate HTTP response
    Maps domain exceptions to appropriate HTTP status codes
    
    Args:
        error: The exception that occurred
        
    Returns:
        HTTP error response with appropriate status code
    """
    error_type = type(error).__name__
    error_message = str(error)
    
    if isinstance(error, UserAlreadyExistsException):
        logger.warning("user_already_exists", error_type=error_type, error=error_message)
        return create_error_response(error_message, 409)
    
    elif isinstance(error, InvalidCredentialsException):
        logger.warning("invalid_credentials", error_type=error_type)
        return create_error_response(error_message, 401)
    
    elif isinstance(error, (UserNotFoundException, InvalidTokenException)):
        logger.warning("resource_not_found", error_type=error_type, error=error_message)
        return create_error_response(error_message, 404)
    
    elif isinstance(error, ValueError):
        logger.warning("validation_error", error_type=error_type, error=error_message)
        return create_error_response(error_message, 400)
    
    elif isinstance(error, DomainException):
        logger.warning("domain_error", error_type=error_type, error=error_message)
        return create_error_response(error_message, 400)
    
    else:
        # Don't expose internal error details in production
        logger.error("internal_server_error", error_type=error_type, error=error_message, exc_info=True)
        return create_error_response('Internal server error', 500)
