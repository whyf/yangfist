import subprocess
from pipes import Template

import allure
import pytest
import arrow
import os
import random

from cachetools import cached
from psutil import users

from config.configHandler import ConfigHandler
from utils.log_utils import logger
"""
利用csv数据分别生成page.py 和case.py，这个是page.py模板文件
"""
@allure.epic("方顷科技智慧后勤")
@allure.feature("保洁管理")
class TestCase():
    @allure.story("保洁工单")
    @allure.title("保洁工单_新增保洁工单")
    def test_add_protocol_list(self, login):
        #发请求
        d1 = login.IotplatDeviceModule.api("物联网", "协议管理-成功获取协议列表").response(login_user="user2")
        #断言
        login.IotplatDeviceModule.iotplat_device_assert(d1,"物联网","协议管理-成功获取协议列表")