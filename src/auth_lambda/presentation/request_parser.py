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


def extract_path_parameter(event: Dict[str, Any], param_name: str, route_prefix: str = None) -> str:
    """
    Extrai um parâmetro do path da requisição de forma dinâmica.

    Suporta múltiplos formatos de path do API Gateway:
    - pathParameters direto: {'user_id': '123'}
    - pathParameters com proxy: {'proxy': 'user-by-id/123'}
    - rawPath ou path: '/auth/user-by-id/123'

    Args:
        event: Evento do Lambda
        param_name: Nome do parâmetro a ser extraído
        route_prefix: Prefixo da rota antes do parâmetro (ex: 'user-by-id', 'items', 'orders')
                     Se não fornecido, extrai o último segmento do path

    Returns:
        Valor do parâmetro extraído

    Examples:
        # Para rota /auth/user-by-id/123 com proxy
        user_id = extract_path_parameter(event, 'user_id', 'user-by-id')  # '123'

        # Para rota /items/abc-456 com proxy
        item_id = extract_path_parameter(event, 'item_id', 'items')  # 'abc-456'

        # Para rota /orders/order-789/details com proxy
        order_id = extract_path_parameter(event, 'order_id', 'orders')  # 'order-789'

        # Sem route_prefix, pega o último segmento
        last_segment = extract_path_parameter(event, 'id')  # Último segmento do path
    """
    path_parameters = event.get('pathParameters', {})

    # Tenta obter o parâmetro diretamente
    value = path_parameters.get(param_name)

    # Se não encontrou e existe um parâmetro 'proxy', extrai do proxy
    if not value and 'proxy' in path_parameters:
        proxy_path = path_parameters['proxy']

        if route_prefix:
            # Extrai do formato "{route_prefix}/{param_value}"
            search_pattern = f'{route_prefix}/'
            if search_pattern in proxy_path:
                parts = proxy_path.split(search_pattern)
                if len(parts) > 1:
                    # Pega a primeira parte após o prefixo (antes de qualquer outra /)
                    value = parts[1].split('/')[0].strip()
        else:
            # Se não tem route_prefix, pega o último segmento do path
            segments = [s for s in proxy_path.split('/') if s]
            if segments:
                value = segments[-1]

    # Se ainda não encontrou, tenta extrair do path completo
    if not value:
        path = event.get('rawPath', event.get('path', ''))

        if route_prefix:
            search_pattern = f'{route_prefix}/'
            if search_pattern in path:
                parts = path.split(search_pattern)
                if len(parts) > 1:
                    # Pega a primeira parte após o prefixo (antes de qualquer outra /)
                    value = parts[1].split('/')[0].strip()
        else:
            # Se não tem route_prefix, pega o último segmento do path
            segments = [s for s in path.split('/') if s]
            if segments:
                value = segments[-1]

    if not value:
        raise ValueError(f'{param_name} is required')

    return value


def get_route_info(event: Dict[str, Any]) -> tuple[str, str]:
    # API Gateway v2 (HTTP API) usa formato diferente
    if 'requestContext' in event and 'http' in event['requestContext']:
        path = event.get('rawPath', '')
        http_method = event['requestContext']['http']['method']
    else:
        # Fallback para API Gateway v1 (REST API)
        path = event.get('path', '')
        http_method = event.get('httpMethod', '')

    return path, http_method
