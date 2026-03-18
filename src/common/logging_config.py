import structlog
import orjson
import logging

def orjson_dumps(obj, **kwargs):
    return orjson.dumps(obj).decode('utf-8')


def reorder_and_filter_keys(logger, method_name, event_dict):
    ordered = {}
    if 'timestamp' in event_dict:
        ordered['timestamp'] = event_dict.pop('timestamp')
    if 'level' in event_dict:
        ordered['level'] = event_dict.pop('level')
    if 'event' in event_dict:
        ordered['event'] = event_dict.pop('event')
    ordered.update(event_dict)
    return ordered


def configure_logging(level: str = "INFO"):
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    for handler in root_logger.handlers:
        handler.setLevel(numeric_level)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,   # 🔴 ESSENCIAL
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.format_exc_info,
            reorder_and_filter_keys,
            structlog.processors.JSONRenderer(serializer=orjson_dumps),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None) -> structlog.stdlib.BoundLogger:
    if name is None:
        name = __name__
    return structlog.get_logger(name)


configure_logging()
