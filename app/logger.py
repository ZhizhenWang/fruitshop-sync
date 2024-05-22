import logging.config

from app.config import log_config

# Define a global variable to check if logging is configured
_logging_configured = False


def get_logger(name='sync_logger'):
    global _logging_configured

    if not _logging_configured:
        # Load the logging configuration
        logging.config.dictConfig(log_config)
        _logging_configured = True

    # Return the requested logger
    return logging.getLogger(name)
