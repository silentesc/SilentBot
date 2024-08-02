import logging
import datetime


logger = logging.getLogger("logger")
log_file_name = f"logs/{datetime.datetime.now().strftime("%Y-%m-%d")}.log"


def log_info(message):
    logging.basicConfig(filename=log_file_name, level=logging.INFO, format="[%(levelname)s] [%(asctime)s] [%(module)s:%(funcName)s:%(lineno)d] %(message)s")
    logger.info(message)


def log_error(message):
    logging.basicConfig(filename=log_file_name, level=logging.ERROR, format="[%(levelname)s] [%(asctime)s] [%(filename)s:%(funcName)s:%(lineno)d] %(message)s")
    logger.error(message)
