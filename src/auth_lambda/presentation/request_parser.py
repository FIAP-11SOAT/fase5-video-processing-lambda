import json
from typing import Dict, Any


def parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
    body_str = event.get('body', '{}')
    try:
        return json.loads(body_str)
    except json.JSONDecodeError:
        raise ValueError('Invalid JSON in request body')


def extract_bearer_token(event: Dict[str, Any]) -> str:
    headers = event.get('headers', {})
    auth_header = headers.get('Authorization') or headers.get('authorization')

    if not auth_header:
        raise ValueError('Authorization header is required')

    if not auth_header.startswith('Bearer '):
        raise ValueError('Authorization header must use Bearer scheme')

    return auth_header.replace('Bearer ', '')

def extract_ms_token(event: Dict[str, Any]) -> str:
    headers = event.get('headers', {})
    ms_token = headers.get('X-MS-Token') or headers.get('x-ms-token')

    if not ms_token:
        raise ValueError('X-MS-Token header is required')

    return ms_token


def extract_path_parameter(event: Dict[str, Any], param_name: str) -> str:
    path_parameters = event.get('pathParameters', {})
    value = path_parameters.get(param_name)

    if not value:
        raise ValueError(f'{param_name} is required')

    return value


def get_route_info(event: Dict[str, Any]) -> tuple[str, str]:
    path = event.get('path', '')
    http_method = event.get('httpMethod', '')
    return path, http_method
