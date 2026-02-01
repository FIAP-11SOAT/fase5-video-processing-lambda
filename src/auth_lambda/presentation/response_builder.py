import json
from typing import Dict, Any


def create_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
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
    return create_response(status_code, data)


def create_error_response(error: str, status_code: int = 500) -> Dict[str, Any]:
    return create_response(status_code, {'error': error})
