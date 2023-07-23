import logging
from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    DATE_FORMAT: str = "%d/%m/%Y, %H:%M:%S"

    LOG_NAME: str = "steroid"
    LOG_FORMAT: str = "[%(asctime)s] %(levelname)s %(message)s"
    LOG_LEVEL: str = "INFO"

    UVICORN_ACCESS_LOG_FORMAT: str = '[%(asctime)s] %(levelname)s [Uvicorn] %(client_addr)s - "%(request_line)s" %(status_code)s'

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": DATE_FORMAT,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": UVICORN_ACCESS_LOG_FORMAT,
            "datefmt": DATE_FORMAT,
            "use_colors": False,
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "error": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        LOG_NAME: {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": LOG_LEVEL,
        },
        "uvicorn.error": {
            "handlers": ["error"],
            "level": LOG_LEVEL,
        },
    }


def getLogConfig():
    return LogConfig().model_dump()


logger = None


def getLogger(disableAccessLog: bool = False, disableErrorLog: bool = True):
    """
    If the logger is not created yet, create it.
    Otherwise, return the logger.
    This is to avoid creating multiple loggers.
    This is a singleton pattern.
    https://en.wikipedia.org/wiki/Singleton_pattern
    """

    global logger

    if not logger:
        dictConfig(getLogConfig())
        logger = logging.getLogger(LogConfig().LOG_NAME)

        logging.getLogger("uvicorn.access").disabled = disableAccessLog
        logging.getLogger("uvicorn.error").disabled = disableErrorLog

    return logger
