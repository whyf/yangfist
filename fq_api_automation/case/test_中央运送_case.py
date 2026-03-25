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
    #中央运送相关内容
    @allure.story("中央运送")
    @allure.title("运送列表-新增运送单")
    def test_transport_add(self, login):
        #获取发起和接收人员信息
        res1 = login.IlogTransportModule.api("中央运送", "运送列表-人员列表").response(login_user="user2", cached=False)
        userid1 = res1.json().get('data').get('content')[0].get('id')
        username1 = res1.json().get('data').get('content')[0].get('nickName')
        userphone1 = res1.json().get('data').get('content')[0].get('phone')
        depart1 = res1.json().get('data').get('content')[1].get('defaultDepart')
        userid2 = res1.json().get('data').get('content')[1].get('id')
        username2 = res1.json().get('data').get('content')[1].get('nickName')
        userphone2 = res1.json().get('data').get('content')[1].get('phone')
        depart2 = res1.json().get('data').get('content')[1].get('defaultDepart')
        # 获取位置信息
        res2 = login.IlogTransportModule.api("中央运送", "运送列表-位置信息").response(login_user="user2", cached=False)
        areaid1 = res2.json().get('data')[0].get('id')
        areaname1 = res2.json().get('data')[0].get('nickName')
        areaid2 = res2.json().get('data')[1].get('id')
        areaname2 = res2.json().get('data')[1].get('nickName')
        # 获取运输对象信息
        res3 = login.IlogTransportModule.api("中央运送", "运送对象-列表").response(login_user="user2", cached=False)
        objectid = res3.json().get('data').get('content')[0].get('id')
        objectname = res3.json().get('data').get('content')[0].get('nickName')
        formMatters = res3.json().get('data').get('content')[0].get('formMatters')
        formMatters = formMatters.replace("\"","\\\"")
        methodid = res3.json().get('data').get('content')[0].get('dictIds')[0]
        values = {
            "userid1":userid1,
            "username1":username1,
            "userphone1":userphone1,
            "depart1":depart1,
            "userid2":userid2,
            "username2":username2,
            "userphone2":userphone2,
            "depart2":depart2,
            "areaid1":areaid1,
            "areaname1":areaname1,
            "areaid2":areaid2,
            "areaname2":areaname2,
            "objectid":objectid,
            "objectname":objectname,
            "formMatters":formMatters,
            "methodid":methodid
        }
        #新增运送单
        d1 = login.IlogTransportModule.api("中央运送", "运送列表-新增运送单").response(login_user="user1", Template_values=values)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送列表-新增运送单")
    @allure.story("中央运送")
    @allure.title("运送列表-运送单详情")
    def test_transport_detail(self, login):
        #获取运送单id
        res1 = login.IlogTransportModule.api("中央运送", "运送列表-运送单列表").response(login_user="user2", cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看运输单详情
        d1 = login.IlogTransportModule.api("中央运送", "运送列表-运送单详情").response(login_user="user2", Template_values={"id":id})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送列表-运送单详情")


    @allure.story("中央运送")
    @allure.title("运送列表-编辑运送单")
    def test_transport_edit(self, login):
        #获取运送单id
        res4 = login.IlogTransportModule.api("中央运送", "运送列表-运送单列表").response(login_user="user2", cached=False)
        id = res4.json().get('data').get('content')[0].get('id')
        #获取发起和接收人员信息
        res1 = login.IlogTransportModule.api("中央运送", "运送列表-人员列表").response(login_user="user2", cached=False)
        userid1 = res1.json().get('data').get('content')[0].get('id')
        username1 = res1.json().get('data').get('content')[0].get('nickName')
        userphone1 = res1.json().get('data').get('content')[0].get('phone')
        depart1 = res1.json().get('data').get('content')[1].get('defaultDepart')
        userid2 = res1.json().get('data').get('content')[1].get('id')
        username2 = res1.json().get('data').get('content')[1].get('nickName')
        userphone2 = res1.json().get('data').get('content')[1].get('phone')
        depart2 = res1.json().get('data').get('content')[1].get('defaultDepart')
        #获取位置信息
        res2 = login.IlogTransportModule.api("中央运送", "运送列表-位置信息").response(login_user="user2", cached=False)
        areaid1 = res2.json().get('data')[0].get('id')
        areaname1 = res2.json().get('data')[0].get('nickName')
        areaid2 = res2.json().get('data')[1].get('id')
        areaname2 = res2.json().get('data')[1].get('nickName')
        #获取运输对象信息
        res3 = login.IlogTransportModule.api("中央运送", "运送对象-列表").response(login_user="user2", cached=False)
        objectid = res3.json().get('data').get('content')[0].get('id')
        objectname = res3.json().get('data').get('content')[0].get('nickName')
        formMatters = res3.json().get('data').get('content')[0].get('formMatters')
        print(formMatters)
        formMatters = formMatters.replace("\"","\\\"")
        print(formMatters)
        methodid = res3.json().get('data').get('content')[0].get('dictIds')[0]
        values = {
            "userid1":userid1,
            "username1":username1,
            "userphone1":userphone1,
            "depart1":depart1,
            "userid2":userid2,
            "username2":username2,
            "userphone2":userphone2,
            "depart2":depart2,
            "areaid1":areaid1,
            "areaname1":areaname1,
            "areaid2":areaid2,
            "areaname2":areaname2,
            "objectid":objectid,
            "objectname":objectname,
            "formMatters":formMatters,
            "methodid":methodid,
            "id":id
        }
        #编辑运送单
        d1 = login.IlogTransportModule.api("中央运送", "运送列表-编辑运送单").response(login_user="user2", Template_values=values)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送列表-编辑运送单")


    @allure.story("中央运送")
    @allure.title("运送列表-运送列表-派单")
    def test_transport_sendorders(self, login):
        #获取运送单id
        res1 = login.IlogTransportModule.api("中央运送", "运送列表-运送单列表").response(login_user="user2", cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #获取可接单人员信息
        res2 = login.IlogTransportModule.api("中央运送", "运送列表-派单人员列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[1].get('id')
        #发起派单
        d1 = login.IlogTransportModule.api("中央运送", "运送列表-派单").response(login_user="user2", Template_values={"id":id,"userid":userid})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送列表-派单")

    @allure.story("中央运送")
    @allure.title("运送列表-运送列表筛选")
    def test_transport_filtrate(self, login):
        #获取运送单号
        res1 = login.IlogTransportModule.api("中央运送", "运送列表-运送单列表").response(login_user="user2", cached=False)
        id = res1.json().get('data').get('content')[0].get('code')
        #运送列表查询
        d1 = login.IlogTransportModule.api("中央运送", "运送列表-运送列表筛选").response(login_user="user2", Template_values={"id":id})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送列表-运送列表筛选")


    @allure.story("中央运送")
    @allure.title("运送对象-新增")
    def test_transport_object_add(self, login):
        #获取运送方式
        res1 = login.IlogTransportModule.api("中央运送", "运送对象-运送方式列表").response(login_user="user2", cached=False)
        id = res1.json().get('data')[0].get('id')
        #新增运送对象
        d1 = login.IlogTransportModule.api("中央运送", "运送对象-新增").response(login_user="user2", Template_values={"id":id})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送对象-新增")


    @allure.story("中央运送")
    @allure.title("运送对象-编辑")
    def test_transport_object_edit(self, login):
        #获取运送对象id
        res1 = login.IlogTransportModule.api("中央运送", "运送对象-列表").response(login_user="user2", cached=False)
        objectid = res1.json().get('data').get('content')[0].get('id')
        #获取运送方式
        res2 = login.IlogTransportModule.api("中央运送", "运送对象-运送方式列表").response(login_user="user2", cached=False)
        id = res2.json().get('data')[0].get('id')
        #编辑运送方式
        d1 = login.IlogTransportModule.api("中央运送", "运送对象-编辑").response(login_user="user2", Template_values={"id":id,"objectid":objectid})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送对象-编辑")


    @allure.story("中央运送")
    @allure.title("运送对象-删除")
    def test_transport_object_delete(self, login):
        #获取运送对象id
        res1 = login.IlogTransportModule.api("中央运送", "运送对象-列表").response(login_user="user2", cached=False)
        objectid = res1.json().get('data').get('content')[0].get('id')
        #删除运送对象
        d1 = login.IlogTransportModule.api("中央运送", "运送对象-删除").response(login_user="user2", Template_values={"objectid":objectid})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送对象-删除")


    @allure.story("中央运送")
    @allure.title("运送对象-详情")
    def test_transport_object_detail(self, login):
        #获取运送对象id
        res1 = login.IlogTransportModule.api("中央运送", "运送对象-列表").response(login_user="user2", cached=False)
        objectid = res1.json().get('data').get('content')[0].get('id')
        #查看详情
        d1 = login.IlogTransportModule.api("中央运送", "运送对象-详情").response(login_user="user2", Template_values={"objectid":objectid})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送对象-编辑")

    @allure.story("中央运送")
    @allure.title("运送对象-详情")
    def test_transport_object_filtrate(self, login):
        #获取运送对象名称
        res1 = login.IlogTransportModule.api("中央运送", "运送对象-列表").response(login_user="user2", cached=False)
        name = res1.json().get('data').get('content')[0].get('nickName')
        #运送对象筛选
        d1 = login.IlogTransportModule.api("中央运送", "运送对象-筛选").response(login_user="user2", Template_values={"name":name})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "运送对象-筛选")


    @allure.story("中央运送")
    @allure.title("移动端-运送列表")
    def test_transport_mobile_list(self, login):
        #运送列表
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送列表").response(login_user="user2", cached=False)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送列表")

    @allure.story("中央运送")
    @allure.title("移动端-运送任务-今日概况")
    def test_transport_mobile_todaysum(self, login):
        #今日概况
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-今日概况").response(login_user="user2", cached=False)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-今日概况")

    @allure.story("中央运送")
    @allure.title("移动端-运送任务-工单池数量")
    def test_transport_mobile_canTakesum(self, login):
        #工单池数量
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-工单池数量").response(login_user="user2", cached=False)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-工单池数量")

    @allure.story("中央运送")
    @allure.title("移动端-运送任务-工单池列表")
    def test_transport_mobile_canTakelist(self, login):
        #工单池列表
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-工单池列表").response(login_user="user2", cached=False)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-工单池列表")

    @allure.story("中央运送")
    @allure.title("移动端-运送任务-转派给我")
    def test_transport_mobile_myDispatchListtome(self, login):
        #工单池列表
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-转派给我").response(login_user="user2", cached=False)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-转派给我")

    @allure.story("中央运送")
    @allure.title("移动端-运送任务-转派他人")
    def test_transport_mobile_myDispatchListtoanother(self, login):
        #工单池列表
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-转派他人").response(login_user="user2", cached=False)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-转派他人")

    @allure.story("中央运送")
    @allure.title("移动端-运送任务-历史工单")
    def test_transport_mobile_historyList(self, login):
        #工单池列表
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-历史工单").response(login_user="user2", cached=False)
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-历史工单")

    @allure.story("中央运送")
    @allure.title("移动端-运送任务-送达")
    def test_transport_mobile_completeorder(self, login):
        # 获取工单id
        res1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-工单池列表").response(login_user="user2", cached=False)
        orderid = res1.json().get('data').get('content')[0].get('id')
        code = res1.json().get('data').get('content')[0].get('code')
        # 接单
        d1 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-接单").response(login_user="user2", cached=False,Template_values={"orderid":orderid})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-接单")
        # 开始工单
        d2 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-开始工单").response(login_user="user2", cached=False,Template_values={"orderid":orderid})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-开始工单")
        # 获取取件码和收件码
        res2 = login.IlogTransportModule.api("中央运送", "运送列表-运送单详情").response(login_user="user2", Template_values={"id":orderid})
        pickupCode = res2.json().get('data').get('pickupCode')
        receivingCode = res2.json().get('data').get('receivingCode')
        # 查看交接码是否开启
        res3 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-交接码状态").response(login_user="user2", cached=False)
        verify = res3.json().get("data")
        if verify:
            pickargument = {
                "code": code,
                "receiptCode": pickupCode
            }
            receivingargument = {
                "code": code,
                "receiptCode": receivingCode
            }
        else:
            pickargument = {
                "code": code,
                "receiptCode": ""
            }
            receivingargument = {
                "code": code,
                "receiptCode": ""
            }
        # 揽件
        d3 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-揽件").response(login_user="user2", cached=False, Template_values ={"pickargument":pickargument})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-揽件")
        # 送达
        d4 = login.IlogTransportModule.api("中央运送", "移动端-运送任务-送达").response(login_user="user2", cached=False, Template_values ={"receivingargument":receivingargument})
        # 断言
        login.IlogTransportModule.ilogtransport_assert(d1, "中央运送", "移动端-运送任务-送达")






if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\jiekou\fq_api_automation\temp'])
    allure_results_dir = r'D:\jiekou\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'/report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
