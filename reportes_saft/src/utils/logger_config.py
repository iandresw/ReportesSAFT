import logging
from logging.handlers import RotatingFileHandler
import os
import sys


def configurar_logger(
    nombre_app="reportes_saft",
    nivel=logging.INFO,
    archivo_log=None
):
    if archivo_log is None:
        base_dir = os.path.dirname(sys.executable)
        archivo_log = os.path.join(base_dir, f"{nombre_app}.log")

    logger = logging.getLogger(nombre_app)
    logger.setLevel(nivel)

    if logger.handlers:
        return logger

    handler = RotatingFileHandler(
        archivo_log,
        maxBytes=2 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
