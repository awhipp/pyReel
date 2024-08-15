"""This module contains a custom logger class to add colors and format the log message."""

import logging


# ANSI escape sequences for colored output
class CustomFormatter(logging.Formatter):
    """Custom formatter to add colors and format the log message."""

    # Define color codes
    COLORS = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
    }
    RESET = "\033[0m"  # Reset color

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


# Set up logging to add timestamps, class, and function names to the output
formatter = CustomFormatter(
    "{levelname}:\t [{asctime} - {name}.{funcName}()] {message}",
    style="{",
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[handler])


def get_logger(name: str) -> logging.Logger:
    """Return a logger object with the given name."""
    return logging.getLogger(name)
