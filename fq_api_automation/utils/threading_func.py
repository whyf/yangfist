#!usr/bin/python
# -*- coding:utf-8一*
import threading


def thread_it(func, **kwargs):
    t = threading.Thread(target=func, kwargs=kwargs)
    t.setDaemon(True)
    t.start()
