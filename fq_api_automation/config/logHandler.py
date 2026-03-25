# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     LogHandler.py
   Description :  日志操作模块
   Author :
   date：
-------------------------------------------------
   Change Activity:
                   2017/03/06: log handler
                   2017/09/21: 屏幕输出/文件输出 可选(默认屏幕和文件均输出)
                   2020/07/13: Windows下TimedRotatingFileHandler线程不安全, 不再使用
-------------------------------------------------
"""
import functools
import traceback
from utils.log_utils import logger
import time

def exception_decorator(performance=False):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            try:
                if performance:
                    start = time.perf_counter()
                    r = func(*args,**kwargs)
                    end = time.perf_counter()
                    logger.info(f'{func.__module__} ,{func.__name__}: {end-start}')
                    return r
                else:
                    return func(*args,**kwargs)
            except Exception as e:
                extra = {
                    'extra_method':func.__name__,
                    'extra_module':func.__module__,
                }
                error_msg_obj ={
                    'exc_info':True,
                    'extra':extra
                }
                #traceback.format_exc()表示哪行代码的错误
                print('ERROR:message:{0},traceback:{1}'.format(str(e),traceback.format_exc()))
                logger.error(str(e),**error_msg_obj)
        return wrapper
    return decorator

if __name__ == '__main__':
    @exception_decorator(1)
    def a():
        print("1"+1)
    a()