import logging.config

LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(filename)s %(lineno)d %(asctime)s\n%(message)s",
            "use_colors": True,
        },
    },
    "handlers": {
        "main": {
            "formatter": "main",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "main": {"handlers": ["main"], "level": "DEBUG"},
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('main')
