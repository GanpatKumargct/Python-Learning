import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger that outputs to stdout and a file.
    This provides standard industry logging for debugging and auditing.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Formatter for log messages
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

# Create a default logger instance for the app
logger = setup_logger("jwt_auth_app")
