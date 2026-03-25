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
@allure.feature("物联网")
class TestCase():
    @allure.story("被服管理")
    @allure.title("被服清洁-被服回收列表")
    def test_get_recycling_list(self, login):
        #发请求
        d1 = login.IlogClothingModule.api("被服管理", "被服清洁-被服回收列表").response(login_user="user2")
        #断言
        login.IlogClothingModule.iotplat_device_assert(d1,"被服管理","被服清洁-被服回收列表")


    @allure.story("被服管理")
    @allure.title("被服清洁-被服回收详情")
    def test_get_recycling_detail(self, login):
        #获取被服id
        res = login.IlogClothingModule.api("被服管理", "被服清洁-被服回收列表").response(login_user="user2",cached=False)
        id = res.json().get('data').get('content')[0].get('id')
        #发请求
        d1 = login.IlogClothingModule.api("被服管理", "被服清洁-被服回收详情").response(login_user="user2",Template_values={"id":id})
        #断言
        login.IlogClothingModule.iotplat_device_assert(d1,"被服管理","被服清洁-被服回收详情")


    @allure.story("被服管理")
    @allure.title("被服清洁-被服回收筛选")
    def test_get_recycling_filtrate(self, login):
        #获取被服回收单号
        res = login.IlogClothingModule.api("被服管理", "被服清洁-被服回收列表").response(login_user="user2",cached=False)
        orderNo = res.json().get('data').get('content')[0].get('orderNo')
        # 发请求
        d1 = login.IlogClothingModule.api("被服管理", "被服清洁-被服回收筛选").response(login_user="user2",Template_values={"orderNo":orderNo})
        #断言
        login.IlogClothingModule.iotplat_device_assert(d1,"被服管理","被服清洁-被服回收筛选")

























if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\jiekou\fq_api_automation\temp'])
    allure_results_dir = r'D:\jiekou\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'D:\jiekou\fq_api_automation\report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
