import logging

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def setup_logging(log_level: int) -> None:
    """Setup logging.

    Args:
        log_level (int): e.g. logging.INFO
    """
    logging.basicConfig(level=log_level, format=LOG_FORMAT)
