import logging
import datetime


class Logger:
    logger = logging.getLogger("logger")
    log_file_name = f"logs/{datetime.datetime.now().strftime("%Y-%m-%d")}.log"

    @staticmethod
    def log_info(message):
        logging.basicConfig(filename=Logger.log_file_name, level=logging.INFO, format="[%(levelname)s] [%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(message)s")
        Logger.logger.info(message)

    @staticmethod
    def log_error(message):
        logging.basicConfig(filename=Logger.log_file_name, level=logging.ERROR, format="[%(levelname)s] [%(asctime)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s")
        Logger.logger.error(message)
