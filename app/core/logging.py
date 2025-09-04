import logging
import sys
from logging import Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler


def setup_logging():
    # Create a logger
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    # Create a formatter
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create a stream handler for console output
    stream_handler = StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Create a file handler for rotating log files
    file_handler = TimedRotatingFileHandler("app.log", when="midnight", interval=1, backupCount=7)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()
