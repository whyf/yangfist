#!usr/bin/python
# -*- coding: utf-8 -*-
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.get_project_name_util import JarProjectUtil

def get_logger(name="root"):
    logger = logging.getLogger(name)
    #print(JarProjectUtil.project_root_path()+"/log/log.log")
    #handler = TimedRotatingFileHandler(filename=JarProjectUtil.project_root_path()+"/log/log.log",when='D',backupCount=7,encoding='UTF-8')
    handler = TimedRotatingFileHandler(filename=JarProjectUtil.project_root_path() + '/log/'+"{}.log".format(time.strftime("%Y-%m-%d")), when='D',
                                       backupCount=7, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    logging_format = logging.Formatter('[%(asctime)s %(levelname)s in  %(module)s: %(message)s] ')
    handler.setFormatter(logging_format)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = get_logger(__name__)

if __name__ == '__main__':
    print(__name__)
    logger.info('123')
    logger.error('123')