import logging
import os
from util.singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        self.logger = logging.getLogger('blockchain')

        log_level = os.getenv('BLOCKCHAIN_LOG_LEVEL', 'INFO')
        self.logger.setLevel(logging.getLevelName(log_level))

        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
