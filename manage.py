import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.DEBUG)
file_log_handler = RotatingFileHandler('logs/log',maxBytes=1024*1024*100,backupCount=10)
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
file_log_handler.setFormatter(formatter)
logging.getLogger().addHandler(file_log_handler)

logging.debug('this is a debug log')