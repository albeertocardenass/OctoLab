import logging
from config import LOG_FILE

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

        fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
        fh.setFormatter(fmt)

        ch = logging.StreamHandler()
        ch.setFormatter(fmt)

        logger.addHandler(fh)
        logger.addHandler(ch)
    return logger
