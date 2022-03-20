import logging
from colorlog import ColoredFormatter, StreamHandler


def get_custom_logger(name):
    formatter = ColoredFormatter(
        "{log_color}{levelname: <9} {asctime} {name}{reset}{blue} -> {message}",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "bold_red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="{",
    )

    handler = StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
