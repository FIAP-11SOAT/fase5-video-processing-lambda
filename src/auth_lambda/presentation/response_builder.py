"""
Response Builder - Helper for creating HTTP responses
This is a shared utility for building consistent API responses
"""
import json
from typing import Dict, Any


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a standardized HTTP response
    
    Args:
        status_code: HTTP status code
        body: Response body as dictionary
        
    Returns:
        API Gateway response format
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
        },
        'body': json.dumps(body)
    }


def create_success_response(data: Dict[str, Any], status_code: int = 200) -> Dict[str, Any]:
    """
    Create a success response
    
    Args:
        data: Success data
        status_code: HTTP status code (default: 200)
        
    Returns:
        API Gateway response format
    """
    return create_response(status_code, data)


def create_error_response(error: str, status_code: int = 500) -> Dict[str, Any]:
    """
    Create an error response
    
    Args:
        error: Error message
        status_code: HTTP status code (default: 500)
        
    Returns:
        API Gateway response format
    """
    return create_response(status_code, {'error': error})
