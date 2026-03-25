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
    #资产验收相关内容
    @allure.story("资产管理")
    @allure.title("资产验收-新增验收")
    def test_acceptanceInfo_add(self,login):
        #获取采购单id
        res1 = login.IlogDeviceModule.api("医疗设备", "资产档案-列表查询").response(login_user="user1", cached=False)
        cgid = res1.json()
        print(cgid)










if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\杨帆\fq_api_automation\temp'])
    allure_results_dir = r'D:\杨帆\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'/report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
