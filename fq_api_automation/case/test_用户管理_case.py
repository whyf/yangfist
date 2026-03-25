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
@allure.feature("用户管理")
class TestCase():

    @allure.story("用户管理")
    @allure.title("新增、查询、查看、编辑、删除人员")
    def test_user(self,login):
        #账号姓名、用户名、手机号
        randomStr=str(random.randint(1001,9999))
        nickname="接口测试"+randomStr
        principal="testA"+randomStr
        phone="1500000"+randomStr

        d1 = login.UserModule.api("用户管理", "人员管理-人员新增").response(Template_values={"nickName":nickname,"principal":principal,"phone":phone},login_user="user3")
        login.UserModule.user_add(d1,"用户管理","人员管理-人员新增")

        d2 = login.UserModule.api("用户管理","人员管理-人员列表查询").response(Template_values={"filterName": nickname},login_user="user3")
        login.UserModule.user_add(d2, "用户管理", "人员管理-人员列表查询")
        userId = d2.json().get('data').get('content')[0].get('id')

        d3 = login.UserModule.api("用户管理", "人员管理-人员详情").response(Template_values={"id": userId},login_user="user3")
        login.UserModule.user_list_search(d3,"用户管理","人员管理-人员详情")

        #编辑手机号
        phone1="1510000"+randomStr
        d4 = login.UserModule.api("用户管理", "人员管理-人员编辑").response(Template_values={"id": userId,"nickName":nickname,"principal":principal,"phone":phone1},login_user="user3")
        login.UserModule.user_list_search(d4,"用户管理","人员管理-人员编辑")
        d5 = login.UserModule.api("用户管理", "人员管理-人员列表查询").response(Template_values={"filterName": nickname},login_user="user3",cached=False)
        phone2 = d5.json().get('data').get('content')[0].get('phone')
        result = login.UserModule.user_detail_search(phone1,phone2)
        assert result

        d6 = login.UserModule.api("用户管理", "人员管理-人员删除").response(Template_values={"id": userId},login_user="user3")
        login.UserModule.user_list_search(d6,"用户管理","人员管理-人员删除")

    @allure.story("用户管理")
    @allure.title("根据ID查询人员部门信息")
    def test_user_info(self,login):
        #用户ID
        UserId="4362b0bb-5724-4efb-96e9-79426c9652fb"

        d1 = login.UserModule.api("用户管理", "人员管理-根据ID查询人员部门信息").response(Template_values={"id":UserId},login_user="user3")
        login.UserModule.user_add(d1,"用户管理","人员管理-根据ID查询人员部门信息")

if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\fq_api_automation\temp'])
    allure_results_dir = r'D:\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'D:\fq_api_automation\report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
