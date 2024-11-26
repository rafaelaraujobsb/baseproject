import logging
import sys

from asgi_correlation_id import correlation_id


def setup_log(log_level: str = "DEBUG"):
    logging_config = {
        "version": 1,
        "filters": {
            "correlation_id": {
                "()": "asgi_correlation_id.CorrelationIdFilter",
                "uuid_length": 32,
                "default_value": "-",
            },
        },
        "formatters": {
            "json": {
                "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "[%(correlation_id)s] %(message)s %(asctime)s %(process)s %(levelname)s %(name)s %(module)s "
                "%(funcName)s %(lineno)s",
            }
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "json",
                "stream": sys.stderr,
                "filters": ["correlation_id"],
            }
        },
        "root": {"level": log_level, "handlers": ["console"], "propagate": True},
    }

    logging.config.dictConfig(logging_config)


def get_correlation_id() -> str:
    return correlation_id.get()
