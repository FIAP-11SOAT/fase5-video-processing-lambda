"""
Request Parser - Extracts data from API Gateway events
This is a shared utility for parsing incoming requests
"""
import json
from typing import Dict, Any, Optional

def parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse JSON body from API Gateway event
    
    Args:
        event: API Gateway event
        
    Returns:
        Parsed JSON body as dictionary
        
    Raises:
        ValueError: If body is missing or invalid JSON
    """
    body_str = event.get('body', '{}')
    try:
        return json.loads(body_str)
    except json.JSONDecodeError:
        raise ValueError('Invalid JSON in request body')

def extract_bearer_token(event: Dict[str, Any]) -> str:
    """
    Extract Bearer token from Authorization header
    
    Args:
        event: API Gateway event
        
    Returns:
        Access token string
        
    Raises:
        ValueError: If Authorization header is missing or invalid
    """
    headers = event.get('headers', {})
    auth_header = headers.get('Authorization') or headers.get('authorization')
    
    if not auth_header:
        raise ValueError('Authorization header is required')
    
    if not auth_header.startswith('Bearer '):
        raise ValueError('Authorization header must use Bearer scheme')
    
    return auth_header.replace('Bearer ', '')

def extract_path_parameter(event: Dict[str, Any], param_name: str) -> str:
    """
    Extract path parameter from API Gateway event
    
    Args:
        event: API Gateway event
        param_name: Name of the path parameter
        
    Returns:
        Path parameter value
        
    Raises:
        ValueError: If path parameter is missing
    """
    path_parameters = event.get('pathParameters', {})
    value = path_parameters.get(param_name)
    
    if not value:
        raise ValueError(f'{param_name} is required')
    
    return value

def get_route_info(event: Dict[str, Any]) -> tuple[str, str]:
    """
    Extract path and HTTP method from event
    
    Args:
        event: API Gateway event
        
    Returns:
        Tuple of (path, http_method)
    """
    path = event.get('path', '')
    http_method = event.get('httpMethod', '')
    return path, http_method
