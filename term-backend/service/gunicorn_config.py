import logging
import warnings

import structlog
from sqlalchemy.exc import SAWarning

from service.monitoring.logger_config import ColorRenderer
from service.settings import Settings

settings = Settings()

bind = ["0.0.0.0:5000"]
worker_class = "uvicorn.workers.UvicornWorker"

timestamper = structlog.processors.TimeStamper(fmt="iso")
pre_chain = [structlog.stdlib.add_log_level, structlog.stdlib.add_logger_name, timestamper]

loglevel = settings.LOG_LEVEL
warnings.filterwarnings("ignore", category=SAWarning)

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": pre_chain,
        },
        "color": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processors": [
                ColorRenderer(),
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            "foreign_pre_chain": pre_chain,
        },
    },
    "handlers": {
        "stdout": {
            "level": loglevel,
            "formatter": "json" if settings.LOG_JSON_FORMAT else "color",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
    "loggers": {
        "gunicorn": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
        "gunicorn.error": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
        "uvicorn": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
        "uvicorn.error": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
        "fastapi": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
        "sqlalchemy.pool.impl.AsyncAdaptedQueuePool": {
            "handlers": ["stdout"],
            "level": logging.CRITICAL,
            "propagate": False,
        },
        "sqlalchemy": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
        "asyncpg": {"handlers": ["stdout"], "level": logging.ERROR, "propagate": False},
        "service": {"handlers": ["stdout"], "level": loglevel, "propagate": False},
    },
}
