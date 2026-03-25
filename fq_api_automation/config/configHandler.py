# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     configHandler
   Description :
   Author :        Laixue
   date：          2024/9/09
-------------------------------------------------
   Change Activity:
                   2024/9/09:
-------------------------------------------------
"""
__author__ = 'ahli'

import os
from config import setting
from utils.lazyProperty import LazyProperty


class ConfigHandler():

    def __init__(self):
        pass

    @LazyProperty
    def grant_type(self):
        print(setting.grant_type)
        return setting.grant_type

    @LazyProperty
    def client_id(self):
        return setting.client_id

    @LazyProperty
    def client_secret(self):
        return setting.client_secret

    @LazyProperty
    def username(self):
        return setting.username


    @LazyProperty
    def password(self):
        return setting.password



    @LazyProperty
    def username2(self):
        return setting.username2


    @LazyProperty
    def password2(self):
        return setting.password2




    @LazyProperty
    def username3(self):
        return setting.username3


    @LazyProperty
    def password3(self):
        return setting.password3


    @LazyProperty
    def username4(self):
        return setting.username4


    @LazyProperty
    def password4(self):
        return setting.password4



    @LazyProperty
    def username5(self):
        return setting.username5


    @LazyProperty
    def password5(self):
        return setting.password5






    @LazyProperty
    def Host(self):
        return setting.Host

    @LazyProperty
    def headers(self):
        return setting.headers

    @LazyProperty
    def login_api(self):
        return setting.login_api

    @LazyProperty
    def excel_path(self):
        return setting.excel_path
