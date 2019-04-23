import logging
from logging.handlers import RotatingFileHandler

from conf import ConfManagement


def setup_log(DevelopmentConfig):
    logging.basicConfig(level=DevelopmentConfig.LOG_LEVEL)
    file_log_handler = RotatingFileHandler(
        "logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)


class DevelopmentConfig(object):
    DEBUG = ConfManagement("project").get_ini("DEBUG")
    LOG_LEVEL = logging.DEBUG


