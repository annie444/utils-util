import os
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


LOG_FORMAT = "[%(asctime)s] %(name)s - %(levelname)s: %(message)s"


def get_level() -> int:
    """Get the logging level based on the environment variable 'LOG_LEVEL'."""
    log_level = os.environ.get("UTILS_LOG_LEVEL", "ERROR").upper()
    levels = {
        "DEBUG": DEBUG,
        "INFO": INFO,
        "WARNING": WARNING,
        "ERROR": ERROR,
        "CRITICAL": CRITICAL,
    }
    return levels.get(log_level, ERROR)
