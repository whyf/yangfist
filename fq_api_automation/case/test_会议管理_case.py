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
from datetime import datetime,timedelta


"""
利用csv数据分别生成page.py 和case.py，这个是page.py模板文件
"""
@allure.epic("方顷科技智慧后勤")
@allure.feature("物联网")
class TestCase():
    #会议管理相关内容
    @allure.story("会议管理")
    @allure.title("会议预约-新建会议室")
    def test_meetingroom(self, login):
        # 新建会议室
        d1 = login.IlogMeetingModule.api("会议管理", "会议预约-新建会议室").response(login_user="user2", cached=False)
        #获取会议室id
        roomid = d1.json().get('data').get('id')
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议预约-新建会议室")
        # 编辑会议室
        d2 = login.IlogMeetingModule.api("会议管理", "会议预约-编辑会议室").response(login_user="user2", cached=False, Template_values = {"roomid": roomid})
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议预约-编辑会议室")
        # 删除会议室
        d3 = login.IlogMeetingModule.api("会议管理", "会议预约-删除会议室").response(login_user="user2", cached=False,Template_values={"roomid": roomid})
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议预约-删除会议室")

    @allure.story("会议管理")
    @allure.title("会议预约-会议室列表")
    def test_meetingroom_list(self, login):
        # 会议室列表
        d1 = login.IlogMeetingModule.api("会议管理", "会议预约-会议室列表").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议预约-会议室列表")


    @allure.story("会议管理")
    @allure.title("会议预约-会议列表")
    def test_meeting_list(self, login):
        # 获取会议室id
        res1 = login.IlogMeetingModule.api("会议管理", "会议预约-会议室列表").response(login_user="user2", cached=False)
        roomid = res1.json().get('data')[0].get('id')
        # 会议列表
        d1 = login.IlogMeetingModule.api("会议管理", "会议预约-会议列表").response(login_user="user2", cached=False,Template_values={"roomid": roomid})
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议预约-会议列表")

    @allure.story("会议管理")
    @allure.title("会议预约-新增会议")
    def test_meeting_add(self, login):
        # 获取会议室id
        res1 = login.IlogMeetingModule.api("会议管理", "会议预约-会议室列表").response(login_user="user2", cached=False)
        roomid = res1.json().get('data')[0].get('id')
        # 获取预约人id
        res2 = login.IlogMeetingModule.api("会议管理", "会议预约-人员列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        #会议时间
        now = datetime.now()+timedelta(days=1)
        date_time = now.strftime("%Y-%m-%d")
        starttime = str(date_time)+r" 10:00:00"
        endtime = str(date_time)+r" 11:00:00"
        # 新建会议
        d1 = login.IlogMeetingModule.api("会议管理", "会议预约-新增会议").response(login_user="user2", cached=False,
        Template_values={"roomid": roomid,"userid":userid,"starttime":starttime,"endtime":endtime})
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议预约-新增会议")


    @allure.story("会议管理")
    @allure.title("会议审核-状态统计")
    def test_meetingaudit_statistics(self, login):
        # 会议审核数量统计
        d1 = login.IlogMeetingModule.api("会议管理", "会议审核-状态统计").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议审核-状态统计")

    @allure.story("会议管理")
    @allure.title("会议审核-列表查询")
    def test_meetingaudit_statistics(self, login):
        # 会议审核列表查询
        d1 = login.IlogMeetingModule.api("会议管理", "会议审核-列表查询").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议审核-列表查询")

    @allure.story("会议管理")
    @allure.title("会议审核-会议审核")
    def test_meetingaudit_approve(self, login):
        # 获取需要审核的会议室id
        res1 = login.IlogMeetingModule.api("会议管理", "会议预约-会议室列表").response(login_user="user2", cached=False)
        responsedata = res1.json().get('data')
        for data in responsedata :
            if data.get("needAudit"):
                roomid = data.get("id")
                break
        # 新建会议
        # 获取预约人id
        res2 = login.IlogMeetingModule.api("会议管理", "会议预约-人员列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        #会议时间
        now = datetime.now()+timedelta(days=2)
        date_time = now.strftime("%Y-%m-%d")
        starttime = str(date_time)+r" 10:00:00"
        endtime = str(date_time)+r" 11:00:00"
        # 新建会议
        res3 = login.IlogMeetingModule.api("会议管理", "会议预约-新增会议").response(login_user="user2", cached=False,
        Template_values={"roomid": roomid,"userid":userid,"starttime":starttime,"endtime":endtime})
        # 获取会议id
        meetingid = res3.json().get('data').get("id")
        #  会议审核
        d1 = login.IlogMeetingModule.api("会议管理", "会议审核-会议审核").response(login_user="user2", cached=False,Template_values={"meetingid": meetingid})

    @allure.story("会议管理")
    @allure.title("会议统计-状态统计")
    def test_meetingstatistics_sum(self, login):
        # 会议统计
        d1 = login.IlogMeetingModule.api("会议管理", "会议统计-状态统计").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议统计-状态统计")

    @allure.story("会议管理")
    @allure.title("会议统计-列表查询")
    def test_meetingstatistics_list(self, login):
        # 会议统计列表查询
        d1 = login.IlogMeetingModule.api("会议管理", "会议统计-列表查询").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议统计-列表查询")

    @allure.story("会议管理")
    @allure.title("会议统计-取消会议")
    def test_meetingstatistics_cancel(self, login):
        # 获取会议id
        res1 = login.IlogMeetingModule.api("会议管理", "会议统计-列表查询").response(login_user="user2", cached=False)
        meetingid = res1.json().get('data').get('content')[0].get('id')
        # 取消会议
        d1 = login.IlogMeetingModule.api("会议管理", "会议统计-取消会议").response(login_user="user2", cached=False,Template_values={"meetingid": meetingid})
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议统计-取消会议")

    @allure.story("会议管理")
    @allure.title("会议设置-会议审核设置")
    def test_meetingsetting(self, login):
        #获取会议室id
        res1 = login.IlogMeetingModule.api("会议管理", "会议预约-会议室列表").response(login_user="user2", cached=False)
        roomid = res1.json().get('data')[0].get('id')
        d1 = login.IlogMeetingModule.api("会议管理", "会议设置-会议审核设置").response(login_user="user2", cached=False,Template_values={"roomid": roomid})
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "会议设置-会议审核设置")


    @allure.story("会议管理")
    @allure.title("移动端-我的预约列表")
    def test_meetingmyappointment_list(self, login):
        # 我的预约列表
        d1 = login.IlogMeetingModule.api("会议管理", "移动端-我的预约列表").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "移动端-我的预约列表")


    @allure.story("会议管理")
    @allure.title("移动端-我的会议列表")
    def test_mymeeting_list(self, login):
        # 我的会议列表
        d1 = login.IlogMeetingModule.api("会议管理", "移动端-我的会议列表").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "移动端-我的会议列表")

    @allure.story("会议管理")
    @allure.title("移动端-历史会议列表")
    def test_meeting_historylist(self, login):
        # 历史会议列表
        d1 = login.IlogMeetingModule.api("会议管理", "移动端-历史会议列表").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "移动端-历史会议列表")

    @allure.story("会议管理")
    @allure.title("移动端-会议审核列表")
    def test_meetingaudit_list(self, login):
        # 会议审核列表
        d1 = login.IlogMeetingModule.api("会议管理", "移动端-会议审核列表").response(login_user="user2", cached=False)
        # 断言
        login.IlogMeetingModule.ilogmeeting_assert(d1, "会议管理", "移动端-会议审核列表")













if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\jiekou\fq_api_automation\temp'])
    allure_results_dir = r'D:\jiekou\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'/report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
