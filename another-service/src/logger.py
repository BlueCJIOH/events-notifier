from typing import Final
import logging

LOGGER: Final[logging.Logger] = logging.getLogger("main_logger")

LOGGER.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
stream_handler.setFormatter(formatter)

LOGGER.addHandler(stream_handler)
