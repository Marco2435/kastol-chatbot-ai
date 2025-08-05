
import logging
import os

def get_logger(name="kastol_logger"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "error.log")

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.ERROR)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
