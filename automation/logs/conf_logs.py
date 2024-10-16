import logging
import json
import pytest

# Configuración del logger
def setup_logger(log_file='test_thales_dev.log'):
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

@pytest.fixture(scope="class", autouse=True)
def test_logger():
    return setup_logger()




def setup_logger_commers(log_file='test_commers_dev_1.log'):
    logger = logging.getLogger('test_logger_commers')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


@pytest.fixture(scope="class", autouse=True)
def test_logger_commers():
    return setup_logger_commers()

