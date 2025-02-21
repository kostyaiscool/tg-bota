import logging.config
from core.config import settings

LOG_LEVEL = settings.log.level

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s %(levelname)s: (%(name)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        'django.channels.server': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'daphne': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    }}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)