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
    @allure.story("物联网")
    @allure.title("协议管理_成功获取协议列表")
    def test_get_protocol_list(self, login):
        #发请求
        d1 = login.IotplatDeviceModule.api("物联网", "协议管理-成功获取协议列表").response(login_user="user2")
        #断言
        login.IotplatDeviceModule.iotplat_device_assert(d1,"物联网","协议管理-成功获取协议列表")


    @allure.story("物联网")
    @allure.title("协议管理_成功新增协议")
    def test_add_protocol(self, login):
        d1 = login.IotplatDeviceModule.api("物联网", "协议管理-成功新增协议").response(Template_values={"nickName":str(random.random())[2:10]+"测试新增协议"})
        login.IotplatDeviceModule.iotplat_device_assert(d1,"物联网","协议管理-成功新增协议")
        res = login.IotplatDeviceModule.api("物联网", "协议管理-成功获取协议列表").response(cached=False)
        id=res.json().get('data').get('content')[0].get('id')
        res1=login.IotplatDeviceModule.api("物联网", "协议管理-成功删除协议").response(Template_values={"id":id})
        res2 = login.IotplatDeviceModule.api("物联网", "协议管理-成功获取协议列表").response(cached=False)
        state=login.IotplatDeviceModule.judge_delete_protocol(res1,res2,id)
        assert state



    @allure.story("物联网")
    @allure.title("协议管理_成功编辑协议")
    def test_edit_protocol(self, login):
        d1 = login.IotplatDeviceModule.api("物联网", "协议管理-成功新增协议").response(
            Template_values={"nickName": str(random.random())[2:10] + "测试新增协议"})
        login.IotplatDeviceModule.iotplat_device_assert(d1, "物联网", "协议管理-成功新增协议")
        res = login.IotplatDeviceModule.api("物联网", "协议管理-成功获取协议列表").response(cached=False)
        id = res.json().get('data').get('content')[0].get('id')
        res1 = login.IotplatDeviceModule.api("物联网", "协议管理-成功编辑协议").response(Template_values={"id": id,"nickName":str(random.random())[2:10]+"测试修改协议"})
        login.IotplatDeviceModule.iotplat_device_assert(res1, "物联网", "协议管理-成功编辑协议")
        login.IotplatDeviceModule.api("物联网", "协议管理-成功删除协议").response(Template_values={"id": id})






    @allure.story("物联网")
    @allure.title("协议管理_成功更改协议启用状态")
    def test_edit_protocol(self, login):
        d1 = login.IotplatDeviceModule.api("物联网", "协议管理-成功新增协议").response(
            Template_values={"nickName": str(random.random())[2:10] + "测试新增协议"})
        login.IotplatDeviceModule.iotplat_device_assert(d1, "物联网", "协议管理-成功新增协议")
        res = login.IotplatDeviceModule.api("物联网", "协议管理-成功获取协议列表").response(cached=False)
        id = res.json().get('data').get('content')[0].get('id')
        res1 = login.IotplatDeviceModule.api("物联网", "协议管理-更新协议启用状态").response(Template_values={"id": id})
        login.IotplatDeviceModule.iotplat_device_assert(res1, "物联网", "协议管理-更新协议启用状态")
        res = login.IotplatDeviceModule.api("物联网", "协议管理-成功获取协议列表").response(cached=False)
        assert  res.json().get('data').get('content')[0].get('enable')
        login.IotplatDeviceModule.api("物联网", "协议管理-成功删除协议").response(Template_values={"id": id})













if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\jiekou\fq_api_automation\temp'])
    allure_results_dir = r'D:\jiekou\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'D:\jiekou\fq_api_automation\report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
