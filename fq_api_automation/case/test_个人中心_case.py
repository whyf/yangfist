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
@allure.feature("个人中心")
class TestCase():
    @allure.story("个人中心")
    @allure.title("个人信息查看")
    def test_get_user_info(self, login):
        #发请求
        d1 = login.UserCenterModule.api("个人中心", "获取用户账号信息").response(Template_values={"access_token":login.access_token})
        #断言
        login.UserCenterModule.user_center_assert(d1,"个人中心","获取用户账号信息")




















if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'C:\fq\fq_api_automation\temp'])
    allure_results_dir = r'C:\fq\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'C:\fq\fq_api_automation\report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
