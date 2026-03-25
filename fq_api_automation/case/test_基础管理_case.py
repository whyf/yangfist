import subprocess
from pipes import Template
import json
import allure
import pytest
import arrow
import os
import random

from cachetools import cached
from psutil import users
from config.configHandler import ConfigHandler
from utils.log_utils import logger

from config.setting import login_api,Host,grant_type,client_id,client_secret,username,password,headers
from utils.get_tokens import get_token
from utils.webRequest import WebRequest
from datetime import datetime


"""
利用csv数据分别生成page.py 和case.py，这个是page.py模板文件
"""
@allure.epic("方顷科技智慧后勤")
@allure.feature("物联网")
class TestCase():
    #合同管理相关内容
    @allure.story("基础管理")
    @allure.title("合同管理-新增")
    def test_contract_add(self, login):
        #获取项目信息
        res1 = login.IlogBasicModule.api("基础管理", "合同管理-获取项目信息").response(login_user="user2",cached=False)
        prjectid = res1.json().get('data')[0].get('id')
        #获取主体信息
        res2 = login.IlogBasicModule.api("基础管理", "合同管理-主体信息").response(login_user="user2",cached=False)
        departid = res2.json().get('data')[0].get('id')
        #获取合同分类
        res3 = login.IlogBasicModule.api("基础管理", "合同管理-合同分类信息").response(login_user="user2",cached=False)
        typeid = res3.json().get('data')[0].get('id')
        #签订时间
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        #签订单位信息
        res4 = login.IlogBasicModule.api("基础管理", "合同管理-签订单位信息").response(login_user="user2",cached=False)
        signingunit = res4.json().get('data')[0].get('id')
        #新增合同
        d1 = login.IlogBasicModule.api("基础管理", "合同管理-新增").response(login_user="user2", cached=False,
        Template_values={"prjectid":prjectid,"departid":departid,"typeid":typeid,"date_time":date_time,"signingunit":signingunit})
        #断言
        login.IlogBasicModule.ilogBasic_assert(d1, "基础管理", "合同管理-新增")
    @allure.story("基础管理")
    @allure.title("合同管理-编辑")
    def test_contract(self, login):
        #获取合同id
        res1 = login.IlogBasicModule.api("基础管理", "合同管理-合同列表").response(login_user="user2",cached=False,Template_values={"filterKey":"杨帆自动化测试"})
        id = res1.json().get('data').get('content')[0].get('id')
        #查看合同详情
        d1 = login.IlogBasicModule.api("基础管理", "合同管理-合同详情").response(login_user="user2",cached=False,Template_values={"id":id})
        #断言
        login.IlogBasicModule.ilogBasic_assert(d1, "基础管理", "合同管理-合同详情")
        # #获取项目id
        projectid = d1.json().get('data').get('projectId')
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        #编辑合同
        d2 = login.IlogBasicModule.api("基础管理", "合同管理-编辑").response(login_user="user2",cached=False,Template_values={"id":id,"date_time":date_time,"projectid":projectid})
        #断言
        login.IlogBasicModule.ilogBasic_assert(d2, "基础管理", "合同管理-编辑")
        #删除合同
        d3 = login.IlogBasicModule.api("基础管理", "合同管理-删除").response(login_user="user2",cached=False,Template_values={"id":id})
        #断言
        login.IlogBasicModule.ilogBasic_assert(d3, "基础管理", "合同管理-删除")

    @allure.story("基础管理")
    @allure.title("合同管理-统计")
    def test_contract_statistics(self, login):
        #销售统计
        d1 = login.IlogBasicModule.api("基础管理", "合同统计-销售统计").response(login_user="user2",cached=False)
        #断言
        login.IlogBasicModule.ilogBasic_assert(d1, "基础管理", "合同统计-销售统计")
        #采购统计
        d2 = login.IlogBasicModule.api("基础管理", "合同统计-采购统计").response(login_user="user2",cached=False)
        #断言
        login.IlogBasicModule.ilogBasic_assert(d2, "基础管理", "合同统计-采购统计")
        #本月概要
        d3 = login.IlogBasicModule.api("基础管理", "合同统计-本月概要").response(login_user="user2",cached=False)
        #断言
        login.IlogBasicModule.ilogBasic_assert(d3, "基础管理", "合同统计-本月概要")
















if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\jiekou\fq_api_automation\temp'])
    allure_results_dir = r'D:\jiekou\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'/report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
