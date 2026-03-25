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
    def test_acceptanceInfo_add(self, login):
        #获取采购单id
        res1 = login.IlogAssetModule.api("资产管理", "资产验收-选择采购单列表").response(login_user="user2", cached=False)
        cgid = res1.json().get('data').get('content')[0].get('id')
        #获取验收资产信息
        res2 = login.IlogAssetModule.api("资产管理", "资产验收-选择物资列表").response(login_user="user2", Template_values={"cgid": cgid})
        contactOrderCount = int(res2.json().get('data').get('materialVos')[0].get('contactOrderCount'))
        procureUnit = res2.json().get('data').get('materialVos')[0].get('procureUnit')
        procureUnitName = res2.json().get('data').get('materialVos')[0].get('procureUnitName')
        procurePrice = res2.json().get('data').get('materialVos')[0].get('procurePrice')
        materialId = res2.json().get('data').get('materialVos')[0].get('materialId')
        fkid = res2.json().get('data').get('materialVos')[0].get('id')
        procureId = res2.json().get('data').get('materialVos')[0].get('procureId')
        procureNo = res2.json().get('data').get('materialVos')[0].get('procureNo')
        checkCount = int(res2.json().get('data').get('materialVos')[0].get('checkCount'))
        materialName = res2.json().get('data').get('materialVos')[0].get('materialName')
        supplierId = res2.json().get('data').get('materialVos')[0].get('supplierId')
        supplierName = res2.json().get('data').get('materialVos')[0].get('supplierName')
        #新增购入验收
        keys = {
            "contactOrderCount":contactOrderCount,
                "procureUnit":procureUnit,
                "procureUnitName":procureUnitName,
                "procurePrice":procurePrice,
                "materialId":materialId,
                "fkid":fkid,
                "procureId":procureId,
                "procureNo":procureNo,
                "checkCount":checkCount,
                "materialName":materialName,
                "supplierId":supplierId,
                "supplierName":supplierName
                }
        d1 = login.IlogAssetModule.api("资产管理", "资产验收-新增购入验收").response(login_user="user2", Template_values=keys)
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产验收-新增购入验收")

        #其他方式登记验收
        source = ["LEASE","DONATION","PROBATION","SELF"]
        for sourcetype in source:

            #获取计量单位信息
            res3 = login.IlogAssetModule.api("资产管理", "资产验收-计量单位列表").response(login_user="user2", cached=False)
            unitname = res3.json().get('data')[0].get('nickName')
            unitid = res3.json().get('data')[0].get('id')
            #发起新增验收
            d2 = login.IlogAssetModule.api("资产管理", "资产验收-新增其他方式验收").response(login_user="user2", Template_values={"unitid": unitid,"unitname":unitname,"sourcetype":sourcetype})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产验收-新增其他方式验收")


    @allure.story("资产管理")
    @allure.title("资产验收-验收列表筛选")
    def test_assert_acceptanceInfo_filtrate(self, login):
        # 获取验收单号
        res1 = login.IlogAssetModule.api("资产管理", "资产验收-验收列表").response(login_user="user2", cached=False)
        #获取验收单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #验收列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产验收-验收列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("资产验收-验收单详情")
    def test_assert_acceptanceInfo_detai(self, login):
        #获取验收单id
        res1 = login.IlogAssetModule.api("资产管理", "资产验收-验收列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看验收详情
        d1 = login.IlogAssetModule.api("资产管理", "资产验收-验收单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产验收-验收单详情")



#资产档案相关内容
    @allure.story("资产管理")
    @allure.title("资产档案-直接登记")
    def test_assert_add(self, login):
    #直接登记购入
        #获取资产分类
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-查看资产分类").response(login_user="user2", cached=False)
        assettype = res1.json().get('data')[0].get('id')
        assettypename = res1.json().get('data')[0].get('nickName')
        #获取位置信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-资产位置选择列表").response(login_user="user2", cached=False)
        areaid = res2.json().get('data')[0].get('id')
        areanickname = res2.json().get('data')[0].get('nickName')
        #获取负责人信息
        res3 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res3.json().get('data').get('content')[0].get('id')
        username = res3.json().get('data').get('content')[0].get('nickName')
        #获取供应商信息
        res4 = login.IlogAssetModule.api("资产管理", "资产档案-供应商列表").response(login_user="user2", cached=False)
        companyid = res4.json().get('data').get('content')[0].get('id')
        companyname = res4.json().get('data').get('content')[0].get('companyName')
        #入库时间
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        #发起直接登记购入请求
        d1 = login.IlogAssetModule.api("资产管理", "资产档案-直接登记购入").response(login_user="user2",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username,"companyid": companyid,"companyname": companyname})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产档案-直接登记购入")
    #直接登记自研自建
        d2 = login.IlogAssetModule.api("资产管理", "资产档案-直接登记自研自建").response(login_user="user2",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username,"companyid": companyid,"companyname": companyname})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d2, "资产管理", "资产档案-直接登记自研自建")
    #直接登记租赁
        d3 = login.IlogAssetModule.api("资产管理", "资产档案-直接登记租赁").response(login_user="user1",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d3, "资产管理", "资产档案-直接登记租赁")
    #直接登记试用
        d4 = login.IlogAssetModule.api("资产管理", "资产档案-直接登记试用").response(login_user="user1",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d4, "资产管理", "资产档案-直接登记试用")
    #直接登记捐赠
        d5 = login.IlogAssetModule.api("资产管理", "资产档案-直接登记捐赠").response(login_user="user1",
        Template_values={"assettype": assettype, "assettypename": assettypename, "date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                         "userid": userid,"username": username})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d5, "资产管理", "资产档案-直接登记捐赠")

    @allure.story("资产管理")
    @allure.title("资产档案-直接登记")
    def test_assert_delete(self, login):
        # 直接登记购入
        # 获取资产分类
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-查看资产分类").response(login_user="user2", cached=False)
        assettype = res1.json().get('data')[0].get('id')
        assettypename = res1.json().get('data')[0].get('nickName')
        # 获取位置信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-资产位置选择列表").response(login_user="user2",cached=False)
        areaid = res2.json().get('data')[0].get('id')
        areanickname = res2.json().get('data')[0].get('nickName')
        # 获取负责人信息
        res3 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res3.json().get('data').get('content')[0].get('id')
        username = res3.json().get('data').get('content')[0].get('nickName')
        # 获取供应商信息
        res4 = login.IlogAssetModule.api("资产管理", "资产档案-供应商列表").response(login_user="user2", cached=False)
        companyid = res4.json().get('data').get('content')[0].get('id')
        companyname = res4.json().get('data').get('content')[0].get('companyName')
        # 入库时间
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        # 发起直接登记购入请求
        res5 = login.IlogAssetModule.api("资产管理", "资产档案-直接登记购入").response(login_user="user2",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username,"companyid": companyid,"companyname": companyname})
        # 获取资产id
        id = res5.json().get("data")
        # 删除资产
        d1 = login.IlogAssetModule.api("资产管理", "资产档案-资产删除").response(login_user="user2", Template_values={"id": id})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产档案-资产删除")




    @allure.story("资产管理")
    @allure.title("资产档案-资产列表筛选")
    def test_assertlist_filtrate(self, login):
        # 获取资产code
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-资产列表").response(login_user="user2", cached=False)
        assetcode = res1.json().get('data').get('content')[0].get('code')
        # 资产列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产档案-资产列表筛选").response(login_user="user2", Template_values={"assetcode": assetcode})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产档案-资产列表筛选")


    @allure.story("资产管理")
    @allure.title("资产档案-资产详情")
    def test_assertlist_detail(self, login):
        # 获取资产id
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-资产列表").response(login_user="user2", cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        d1 = login.IlogAssetModule.api("资产管理", "资产档案-资产详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产档案-资产详情")






    @allure.story("资产管理")
    @allure.title("资产领用-新增领用")
    def test_assert_receive_add(self, login):
        # 获取领用资产
        res1 = login.IlogAssetModule.api("资产管理", "资产领用-获取领用资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #获取领用人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        #新增资产领用
        d1 = login.IlogAssetModule.api("资产管理", "资产领用-新增领用").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,"department":department,"departmentid":departmentid})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产领用-新增领用")


    @allure.story("资产管理")
    @allure.title("资产领用-领用列表筛选")
    def test_assert_receive_filtrate(self, login):
        # 获取领用人信息
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res1.json().get('data').get('content')[0].get('id')
        #领用列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产领用-领用列表筛选").response(login_user="user2", Template_values={"userid": userid})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产领用-领用列表筛选")

    @allure.story("资产管理")
    @allure.title("资产领用-领用单详情")
    def test_assert_receive_detail(self, login):
        #获取领用单id
        res1 = login.IlogAssetModule.api("资产管理", "资产领用-领用列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看领用详情
        d1 = login.IlogAssetModule.api("资产管理", "资产领用-领用单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产领用-领用单详情")




    @allure.story("资产管理")
    @allure.title("资产借用-新增借用")
    def test_assert_borrow_add(self, login):
        # 获取借用人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        # 获取借用资产
        res1 = login.IlogAssetModule.api("资产管理", "资产领用-获取领用资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #归还时间
        now  = datetime.now().date()
        #新增资产借用
        d1 = login.IlogAssetModule.api("资产管理", "资产借用-新增借用").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,
                                "department":department,"departmentid":departmentid,"date":now})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产借用-新增借用")



    @allure.story("资产管理")
    @allure.title("资产借用-借用列表筛选")
    def test_assert_borrow_filtrate(self, login):
        # 获取借用单号
        res1 = login.IlogAssetModule.api("资产管理", "资产借用-借用列表").response(login_user="user2", cached=False)
        #获取借用单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #借用列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产借用-借用列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)


    @allure.story("资产管理")
    @allure.title("资产借用-借用单详情")
    def test_assert_borrow_detail(self, login):
        #获取借用单id
        res1 = login.IlogAssetModule.api("资产管理", "资产借用-借用列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看借用详情
        d1 = login.IlogAssetModule.api("资产管理", "资产借用-借用单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产借用-借用单详情")


    @allure.story("资产管理")
    @allure.title("资产退还-新增退还")
    def test_assert_refund_add(self, login):
        # 获取退还资产
        res1 = login.IlogAssetModule.api("资产管理", "资产退还-获取退还资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #获取退还人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        # #新增资产退还
        d1 = login.IlogAssetModule.api("资产管理", "资产退还-新增退还").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,"department":department,"departmentid":departmentid})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产退还-新增退还")

    @allure.story("资产管理")
    @allure.title("资产退还-退还列表筛选")
    def test_assert_refund_filtrate(self, login):
        # 获取退还单号
        res1 = login.IlogAssetModule.api("资产管理", "资产退还-退还列表").response(login_user="user2", cached=False)
        #获取退还单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #退还列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产退还-退还列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("资产退还-退还单详情")
    def test_assert_refund_detail(self, login):
        #获取退还单id
        res1 = login.IlogAssetModule.api("资产管理", "资产退还-退还列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看退还详情
        d1 = login.IlogAssetModule.api("资产管理", "资产退还-退还单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产退还-退还单详情")



    @allure.story("资产管理")
    @allure.title("资产归还-新增归还")
    def test_assert_restitution_add(self, login):
        # 获取归还资产
        res1 = login.IlogAssetModule.api("资产管理", "资产归还-获取归还资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        assetType = res1.json().get('data').get('content')[0].get('assetType')
        assetTypeName = res1.json().get('data').get('content')[0].get('assetTypeName')
        #获取归还人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        # #新增资产归还
        d1 = login.IlogAssetModule.api("资产管理", "资产归还-新增归还").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,
                                "department":department,"departmentid":departmentid,"assetType":assetType,"assetTypeName":assetTypeName})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产归还-新增归还")

    @allure.story("资产管理")
    @allure.title("资产归还-归还列表筛选")
    def test_assert_restitution_filtrate(self, login):
        # 获取归还单号
        res1 = login.IlogAssetModule.api("资产管理", "资产归还-归还列表").response(login_user="user2", cached=False)
        #获取归还单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #归还列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产归还-归还列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("资产归还-归还单详情")
    def test_assert_restitution_detail(self, login):
        #获取归还单id
        res1 = login.IlogAssetModule.api("资产管理", "资产归还-归还列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看归还详情
        d1 = login.IlogAssetModule.api("资产管理", "资产归还-归还单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产归还-归还单详情")


    @allure.story("资产管理")
    @allure.title("资产调拨-新增调拨")
    def test_assert_allocation_add(self, login):
        # 获取位置信息
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-资产位置选择列表").response(login_user="user2", cached=False)
        areaid1 = res1.json().get('data')[0].get('id')
        areanickname1 = res1.json().get('data')[0].get('nickName')
        areaid2 = res1.json().get('data')[1].get('id')
        areanickname2 = res1.json().get('data')[1].get('nickName')
        #获取资产信息
        res2 = login.IlogAssetModule.api("资产管理", "资产调拨-获取调拨资产").response(login_user="user2", cached=False,Template_values={ "areaid1": areaid1})
        assetid = res2.json().get('data').get('content')[0].get('id')
        assetcode = res2.json().get('data').get('content')[0].get('code')
        assetnickName = res2.json().get('data').get('content')[0].get('nickName')
        assetType = res2.json().get('data').get('content')[0].get('assetType')
        assetTypeName = res2.json().get('data').get('content')[0].get('assetTypeName')
        #获取人员信息
        res3 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res3.json().get('data').get('content')[0].get('id')
        username = res3.json().get('data').get('content')[0].get('nickName')
        department = res3.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res3.json().get('data').get('content')[0].get('departs')[0].get('id')
        #新增资产调拨
        d1 = login.IlogAssetModule.api("资产管理", "资产调拨-新增调拨").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,
                                "department":department,"departmentid":departmentid,"areaid1":areaid1,"areanickname1":areanickname1,"areaid2":areaid2,"areanickname2":areanickname2})


    @allure.story("资产管理")
    @allure.title("资产调拨-调拨列表筛选")
    def test_assert_allocation_filtrate(self, login):
        # 获取调拨单号
        res1 = login.IlogAssetModule.api("资产管理", "资产调拨-调拨列表").response(login_user="user2", cached=False)
        #获取调拨单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #调拨列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产调拨-调拨列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("资产调拨-调拨单详情")
    def test_assert_restitution_detail(self, login):
        #获取调拨单id
        res1 = login.IlogAssetModule.api("资产管理", "资产调拨-调拨列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看调拨详情
        d1 = login.IlogAssetModule.api("资产管理", "资产调拨-调拨单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产调拨-调拨单详情")


    @allure.story("资产管理")
    @allure.title("资产交接-交接单详情")
    def test_assert_handover_add(self, login):
        # 获取交接资产
        res1 = login.IlogAssetModule.api("资产管理", "资产交接-获取交接资产").response(login_user="user", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #获取被交接人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产交接-交接人列表").response(login_user="user2", cached=False)
        userid2 = res2.json().get('data').get('content')[0].get('id')
        username2 = res2.json().get('data').get('content')[0].get('nickName')
        department2 = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid2 = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        #获取交际人信息
        res3 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid1 = res3.json().get('data').get('content')[0].get('id')
        username1 = res3.json().get('data').get('content')[0].get('nickName')
        department1 = res3.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid1 = res3.json().get('data').get('content')[0].get('departs')[0].get('id')
        #新增交接
        d1 = login.IlogAssetModule.api("资产管理", "资产交接-新增交接").response(login_user="user2",
         Template_values={"assetid": assetid, "assetcode": assetcode,"assetnickName": assetnickName, "userid1": userid1,"username1": username1,"department1": department1,
                          "departmentid1": departmentid1,"userid2": userid2,"username2": username2,"department2": department2,
                          "departmentid2": departmentid2})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产交接-新增交接")


    @allure.story("资产管理")
    @allure.title("资产交接-交接列表筛选")
    def test_assert_allocation_filtrate(self, login):
        # 获取交接单号
        res1 = login.IlogAssetModule.api("资产管理", "资产交接-交接列表").response(login_user="user2", cached=False)
        #获取交接单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #交接列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产交接-交接列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("资产交接-交接单详情")
    def test_assert_restitution_detail(self, login):
        #获取交接单id
        res1 = login.IlogAssetModule.api("资产管理", "资产交接-交接列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看交接详情
        d1 = login.IlogAssetModule.api("资产管理", "资产交接-交接单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产交接-交接单详情")


    @allure.story("资产管理")
    @allure.title("资产处置-新增处置")
    def test_assert_dispose_add(self, login):
        #处置类型
        dispositionType = ['SCRAP','SELL','DONATION','RENTING_TERMINATION']

        for distype in dispositionType :
            #获取处置资产
            res1 = login.IlogAssetModule.api("资产管理", "资产处置-获取处置资产").response(login_user="user2", Template_values={"distype": distype})
            assetid = res1.json().get('data').get('content')[0].get('id')
            assetcode = res1.json().get('data').get('content')[0].get('code')
            assetnickName = res1.json().get('data').get('content')[0].get('nickName')
            price = res1.json().get('data').get('content')[0].get('price')
            netValue = res1.json().get('data').get('content')[0].get('netValue')
            #获取处置人信息
            res2 = login.IlogAssetModule.api("资产管理", "资产处置-处置人列表").response(login_user="user2", cached=False)
            userid = res2.json().get('data').get('content')[0].get('id')
            username = res2.json().get('data').get('content')[0].get('nickName')
            department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
            departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
            #新增资产处置
            d1 = login.IlogAssetModule.api("资产管理", "资产处置-新增处置").response(login_user="user2",
             Template_values={"assetid": assetid, "assetcode": assetcode,"assetnickName": assetnickName, "userid": userid,"username": username,"department": department,
                              "departmentid": departmentid,"price": price,"netValue":netValue,"distype": distype})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产处置-新增处置")

    @allure.story("资产管理")
    @allure.title("资产处置-处置列表筛选")
    def test_assert_dispose_filtrate(self, login):
        # 获取处置单号
        res1 = login.IlogAssetModule.api("资产管理", "资产处置-处置列表").response(login_user="user2", cached=False)
        #获取处置单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #处置列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产处置-处置列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("资产处置-处置单详情")
    def test_assert_dispose_detail(self, login):
        #获取处置单id
        res1 = login.IlogAssetModule.api("资产管理", "资产处置-处置列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看处置详情
        d1 = login.IlogAssetModule.api("资产管理", "资产处置-处置单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产处置-处置单详情")


    @allure.story("资产管理")
    @allure.title("资产台账-资产台账列表")
    def test_assert_ledger_AssetLedgerList(self, login):
        #查看资产台账列表
        d1 = login.IlogAssetModule.api("资产管理", "资产台账-资产台账列表").response(login_user="user2",cached=False)
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-资产台账列表")

    @allure.story("资产管理")
    @allure.title("资产台账-资产台账列表筛选")
    def test_assert_ledger_AssetLedgerList_filtrate(self, login):
            # 获取资产code
            res1 = login.IlogAssetModule.api("资产管理", "资产台账-资产台账列表").response(login_user="user2", cached=False)
            code = res1.json().get('data').get('content').get('content')[0].get('code')
            # 台账列表筛选
            d1 = login.IlogAssetModule.api("资产管理", "资产台账-资产台账列表筛选").response(login_user="user2",Template_values={"code": code})
            # 断言返回的数据是搜索的数据
            login.IlogAssetModule.asset_AssetLedgerList_assert(d1, code)


    @allure.story("资产管理")
    @allure.title("资产台账-产权人台账列表")
    def test_assert_ledger_OwnerLedgerList(self, login):
        #查看资产台账列表
        d1 = login.IlogAssetModule.api("资产管理", "资产台账-产权人台账列表").response(login_user="user2",cached=False)
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-产权人台账列表")

    @allure.story("资产管理")
    @allure.title("资产台账-资产台账-产权人台账列表筛选")
    def test_assert_ledger_OwnerLedgerList_filtrate(self, login):
            # 获取产权人姓名
            res1 = login.IlogAssetModule.api("资产管理", "资产台账-产权人台账列表").response(login_user="user2", cached=False)
            head = res1.json().get('data').get('content').get('content')[0].get('head')
            # 台账列表筛选
            d1 = login.IlogAssetModule.api("资产管理", "资产台账-产权人台账列表筛选").response(login_user="user2",Template_values={"head": head})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-产权人台账列表")


    @allure.story("资产管理")
    @allure.title("资产台账-资产台账-资产台账-产权人台账详情")
    def test_assert_ledger_OwnerLedgerList_Detail(self, login):
        # 获取产权人姓名id
        res1 = login.IlogAssetModule.api("资产管理", "资产台账-产权人台账列表").response(login_user="user2",cached=False)
        headid = res1.json().get('data').get('content').get('content')[0].get('headId')
        #查看详情
        d1 = login.IlogAssetModule.api("资产管理", "资产台账-产权人台账详情").response(login_user="user2", Template_values={"headid": headid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-产权人台账列表")


    @allure.story("资产管理")
    @allure.title("资产台账-使用人台账列表")
    def test_assert_ledger_UserLedgerList(self, login):
        #查看资产台账列表
        d1 = login.IlogAssetModule.api("资产管理", "资产台账-使用人台账列表").response(login_user="user2",cached=False)
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-使用人台账列表")

    @allure.story("资产管理")
    @allure.title("资产台账-资产台账-使用人台账列表筛选")
    def test_assert_ledger_UserLedgerList_filtrate(self, login):
            # 获取使用人姓名
            res1 = login.IlogAssetModule.api("资产管理", "资产台账-使用人台账列表").response(login_user="user2", cached=False)
            assetUser = res1.json().get('data').get('content').get('content')[0].get('assetUser')
            # 台账列表筛选
            d1 = login.IlogAssetModule.api("资产管理", "资产台账-使用人台账列表筛选").response(login_user="user2",Template_values={"assetUser": assetUser})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-使用人台账列表")


    @allure.story("资产管理")
    @allure.title("资产台账-资产台账-资产台账-使用人台账详情")
    def test_assert_ledger_UserLedgerList_Detail(self, login):
        # 获取使用人姓名id
        res1 = login.IlogAssetModule.api("资产管理", "资产台账-使用人台账列表").response(login_user="user2",cached=False)
        assetUserId = res1.json().get('data').get('content').get('content')[0].get('assetUserId')
        #查看详情
        d1 = login.IlogAssetModule.api("资产管理", "资产台账-使用人台账详情").response(login_user="user2", Template_values={"assetUserId": assetUserId})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-使用人台账列表")


    @allure.story("资产管理")
    @allure.title("资产台账-盘点台账列表")
    def test_assert_ledger_InventoryLedgerList(self, login):
        #查看资产台账列表
        d1 = login.IlogAssetModule.api("资产管理", "资产台账-盘点台账列表").response(login_user="user2",cached=False)
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-盘点台账列表")

    @allure.story("资产管理")
    @allure.title("资产台账-盘点台账列表筛选")
    def test_assert_ledger_InventoryLedgerList_filtrate(self, login):
            # 获取资产code
            res1 = login.IlogAssetModule.api("资产管理", "资产台账-盘点台账列表").response(login_user="user2", cached=False)
            code = res1.json().get('data').get('content')[0].get('code')
            # 台账列表筛选
            d1 = login.IlogAssetModule.api("资产管理", "资产台账-盘点台账列表筛选").response(login_user="user2",Template_values={"code": code})
            # 断言返回的数据是搜索的数据
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-盘点台账列表筛选")

    @allure.story("资产管理")
    @allure.title("资产台账-盘点台账盘点记录")
    def test_assert_ledger_InventoryLedgerList_Detail(self, login):
            # 获取资产id
            res1 = login.IlogAssetModule.api("资产管理", "资产台账-盘点台账列表").response(login_user="user2", cached=False)
            id = res1.json().get('data').get('content')[0].get('id')
            # 盘点记录
            d1 = login.IlogAssetModule.api("资产管理", "资产台账-盘点台账盘点记录").response(login_user="user2",Template_values={"id": id})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-盘点台账盘点记录")

    @allure.story("资产管理")
    @allure.title("资产台账-验收台账列表")
    def test_assert_ledger_AcceptanceLedgerList(self, login):
        #查看验收台账列表
        d1 = login.IlogAssetModule.api("资产管理", "资产台账-验收台账列表").response(login_user="user2",cached=False)
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-验收台账列表")

    @allure.story("资产管理")
    @allure.title("资产台账-验收台账列表筛选")
    def test_assert_ledger_AcceptanceLedgerList_filtrate(self, login):
            # 获取资产名称
            res1 = login.IlogAssetModule.api("资产管理", "资产台账-验收台账列表").response(login_user="user2", cached=False)
            nickName = res1.json().get('data').get('content')[0].get('nickName')
            # 验收列表筛选
            d1 = login.IlogAssetModule.api("资产管理", "资产台账-验收台账列表筛选").response(login_user="user2",Template_values={"nickName": nickName})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产台账-验收台账列表筛选")


    #资产盘点相关内容
    @allure.story("资产管理")
    @allure.title("资产盘点-新增盘点计划")
    def test_assert_inventory_add(self, login):
        #获取盘点负责人
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点负责人列表").response(login_user="user2", cached=False)
        userid = res1.json().get('data').get('content')[0].get('id')
        username = res1.json().get('data').get('content')[0].get('nickName')
        #获取盘点资产
        res2 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点资产列表").response(login_user="user2", cached=False)
        assetid = res2.json().get('data').get('content')[0].get('id')
        now = datetime.now().date()
        #新增盘点计划
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-新增盘点计划").response(login_user="user2",Template_values={"userid": userid,"username":username,"assetid":assetid,"now":now})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-新增盘点计划")

    @allure.story("资产管理")
    @allure.title("资产盘点-编辑盘点计划")
    def test_assert_inventory_edit(self, login):
        #获取盘点计划id
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点计划列表").response(login_user="user2",cached=False)
        planid = res1.json().get('data').get('content')[0].get('id')
        #获取盘点负责人
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点负责人列表").response(login_user="user2", cached=False)
        userid = res1.json().get('data').get('content')[0].get('id')
        username = res1.json().get('data').get('content')[0].get('nickName')
        #获取盘点资产
        res2 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点资产列表").response(login_user="user2", cached=False)
        assetid = res2.json().get('data').get('content')[0].get('id')
        now = datetime.now().date()
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-编辑盘点计划").response(login_user="user2",Template_values={"userid": userid,"username":username,"assetid":assetid,"now":now,"planid":planid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-编辑盘点计划")


    @allure.story("资产管理")
    @allure.title("资产盘点-删除盘点计划")
    def test_assert_inventory_delete(self, login):
        #获取盘点计划id
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点计划列表").response(login_user="user2",cached=False)
        planid = res1.json().get('data').get('content')[0].get('id')
        #删除盘点计划
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-删除盘点计划").response(login_user="user2",Template_values={"planid": planid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-删除盘点计划")

    @allure.story("资产管理")
    @allure.title("资产盘点-盘点单列表筛选")
    def test_assert_inventory_order_filtrate(self, login):
        #获取盘点任务名称
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单列表").response(login_user="user2",cached=False)
        nickName = res1.json().get('data').get('content')[0].get('nickName')
        #盘点列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单列表筛选").response(login_user="user2",Template_values={"nickName": nickName})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-盘点单列表筛选")


    @allure.story("资产管理")
    @allure.title("资产盘点-盘点资产")
    def test_assert_inventory_submit(self, login):
        #获取盘点单id
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单列表").response(login_user="user2",cached=False)
        orderid = res1.json().get('data').get('content')[0].get('id')
        #获取盘点资产id
        res2 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单资产列表").response(login_user="user2",cached=False,Template_values={"orderid": orderid})
        assetid = res2.json().get('data').get('content')[0].get('id')
        #盘点为正常
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点资产").response(login_user="user2",Template_values={"orderid": orderid,"assetid":assetid,"result":"NORMAL"})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-盘点资产")
        #盘点为亏损
        d2 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点资产").response(login_user="user2",Template_values={"orderid": orderid,"assetid":assetid,"result":"INVENTORY_LOSS"})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-盘点资产")
        #获取盘盈资产id
        res3 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点资产列表").response(login_user="user2", cached=False)
        assetid1 = res3.json().get('data').get('content')[1].get('id')
        #添加盘盈资产
        d3 = login.IlogAssetModule.api("资产管理", "资产盘点-添加盘盈资产").response(login_user="user2",Template_values={"orderid": orderid,"assetid1":assetid1})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-添加盘盈资产")
        #删除盘盈资产
        #获取盘盈资产id
        res4 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单资产列表").response(login_user="user2",cached=False,Template_values={"orderid": orderid})
        listid = res4.json().get('data').get('content')
        for a in listid :
            if  a.get("assetId") == assetid1 :
                assetid2 = a.get("id")
        d4 = login.IlogAssetModule.api("资产管理", "资产盘点-删除盘盈资产").response(login_user="user2",Template_values={"assetid1":assetid2})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-删除盘盈资产")


    @allure.story("资产管理")
    @allure.title("资产盘点-提交盘点单")
    def test_assert_inventory_commit(self, login):
        #获取盘点单id
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单列表").response(login_user="user2",cached=False)
        orderid = res1.json().get('data').get('content')[0].get('id')
        #提交盘点单
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-提交盘点单").response(login_user="user2",cached=False,Template_values={"orderid": orderid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-提交盘点单")

    @allure.story("资产管理")
    @allure.title("资产盘点-重新盘点")
    def test_assert_inventory_reinvent(self, login):
        #获取盘点单id
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单列表").response(login_user="user2",cached=False)
        orderid = res1.json().get('data').get('content')[0].get('id')
        #重新盘点
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-重新盘点").response(login_user="user2",cached=False,Template_values={"orderid": orderid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-重新盘点")

    #盘点任务相关内容
    @allure.story("资产管理")
    @allure.title("资产盘点-盘点任务列表筛选")
    def test_assert_inventory_task_filtrate(self, login):
        #获取盘点任务单号
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点任务列表").response(login_user="user2",cached=False)
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #盘点任务列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点任务列表筛选").response(login_user="user2",Template_values={"orderNumber": orderNumber})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-盘点任务列表筛选")

    @allure.story("资产管理")
    @allure.title("资产盘点-未盘点人员提醒")
    def test_assert_inventory_task_message(self, login):
        #获取盘点任务单号
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点任务列表").response(login_user="user2",cached=False)
        taskid = res1.json().get('data').get('content')[0].get('id')
        #提醒盘点
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-未盘点人员提醒").response(login_user="user2",Template_values={"taskid": taskid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-未盘点人员提醒")

    @allure.story("资产管理")
    @allure.title("资产盘点-提交盘点任务")
    def test_assert_inventory_task_commit(self, login):
        #获取盘点单id
        res1 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点单列表").response(login_user="user2",cached=False)
        orderid = res1.json().get('data').get('content')[0].get('id')
        #提交盘点单
        res2 = login.IlogAssetModule.api("资产管理", "资产盘点-提交盘点单").response(login_user="user2",cached=False,Template_values={"orderid": orderid})
        #获取盘点任务单号
        res3 = login.IlogAssetModule.api("资产管理", "资产盘点-盘点任务列表").response(login_user="user2",cached=False)
        taskid = res3.json().get('data').get('content')[0].get('id')
        #提交盘点任务
        d1 = login.IlogAssetModule.api("资产管理", "资产盘点-提交盘点任务").response(login_user="user2",Template_values={"taskid": taskid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产盘点-提交盘点任务")


    #资产配额相关内容
    @allure.story("资产管理")
    @allure.title("资产配额-新增")
    def test_assert_quota_add(self, login):
        #获取科室信息
        res1 = login.IlogAssetModule.api("资产管理", "资产配额-科室列表").response(login_user="user2",cached=False)
        departmentid = res1.json().get('data')[0].get('id')
        #获取资产类型
        res2 = login.IlogAssetModule.api("资产管理", "资产配额-资产类型列表").response(login_user="user2",cached=False)
        assettypeid = res2.json().get('data')[0].get('id')
        #新增资产配额
        d1 = login.IlogAssetModule.api("资产管理", "资产配额-新增").response(login_user="user2",Template_values={"departmentid": departmentid,"assettypeid":assettypeid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产配额-新增")

    @allure.story("资产管理")
    @allure.title("资产配额-编辑")
    def test_assert_quota_edit(self, login):
        #获取科室信息
        res1 = login.IlogAssetModule.api("资产管理", "资产配额-科室列表").response(login_user="user2",cached=False)
        departmentid = res1.json().get('data')[0].get('id')
        #获取资产类型
        res2 = login.IlogAssetModule.api("资产管理", "资产配额-资产类型列表").response(login_user="user2",cached=False)
        assettypeid = res2.json().get('data')[0].get('id')
        #获取配额方案id
        res3 = login.IlogAssetModule.api("资产管理", "资产配额-列表").response(login_user="user2",cached=False)
        id = res3.json().get('data').get('content')[0].get('id')
        #获取配额方案事项id
        res4 = login.IlogAssetModule.api("资产管理", "资产配额-详情").response(login_user="user2",cached=False,Template_values={"id": id})
        itemid = res4.json().get('data').get("items")[0].get('id')
        #编辑配额方案
        d1 = login.IlogAssetModule.api("资产管理", "资产配额-编辑").response(login_user="user2",Template_values={"departmentid": departmentid,"assettypeid":assettypeid,"id":id,"itemid":itemid})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产配额-编辑")

    @allure.story("资产管理")
    @allure.title("资产配额-删除方案")
    def test_assert_quota_delete(self, login):
        #获取配额方案id
        res3 = login.IlogAssetModule.api("资产管理", "资产配额-列表").response(login_user="user2",cached=False)
        id = res3.json().get('data').get('content')[0].get('id')
        #删除方案
        d1 = login.IlogAssetModule.api("资产管理", "资产配额-删除方案").response(login_user="user2",cached=False,Template_values={"id": id})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产配额-删除方案")

    @allure.story("资产管理")
    @allure.title("资产配额-列表筛选")
    def test_assert_quota_filtrate(self, login):
        #获取方案名称
        res1 = login.IlogAssetModule.api("资产管理", "资产配额-列表").response(login_user="user2",cached=False)
        name = res1.json().get('data').get('content')[0].get('nickName')
        #方案列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "资产配额-列表筛选").response(login_user="user2",cached=False,Template_values={"name": name})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "资产配额-列表筛选")


    #折旧设置相关内容
    @allure.story("资产管理")
    @allure.title("折旧设置-新增")
    def test_assert_depreciation_add(self, login):
        #获取资产类型
        res1 = login.IlogAssetModule.api("资产管理", "资产配额-资产类型列表").response(login_user="user2",cached=False)
        assettypeid = res1.json().get('data')[0].get('id')
        name = res1.json().get('data')[0].get('nickName')
        #新增折旧方案
        d1 = login.IlogAssetModule.api("资产管理", "折旧设置-新增").response(login_user="user2",cached=False,Template_values={"assettypeid": assettypeid,"name":name})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "折旧设置-新增")


    @allure.story("资产管理")
    @allure.title("折旧设置-编辑")
    def test_assert_depreciation_edit(self, login):
        #获取资产类型
        res1 = login.IlogAssetModule.api("资产管理", "资产配额-资产类型列表").response(login_user="user2",cached=False)
        assettypeid = res1.json().get('data')[0].get('id')
        name = res1.json().get('data')[0].get('nickName')
        #获取方案id
        res2 = login.IlogAssetModule.api("资产管理", "折旧设置-列表").response(login_user="user2",cached=False)
        id = res2.json().get('data').get('content')[0].get('id')
        #编辑折旧方案
        d1 = login.IlogAssetModule.api("资产管理", "折旧设置-编辑").response(login_user="user2",cached=False,Template_values={"assettypeid": assettypeid,"name":name,"id":id})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "折旧设置-编辑")


    @allure.story("资产管理")
    @allure.title("折旧设置-删除")
    def test_assert_depreciation_edit(self, login):
        #获取方案id
        res2 = login.IlogAssetModule.api("资产管理", "折旧设置-列表").response(login_user="user2",cached=False)
        id = res2.json().get('data').get('content')[0].get('id')
        #删除方案
        d1 = login.IlogAssetModule.api("资产管理", "折旧设置-删除").response(login_user="user2",cached=False,Template_values={"id":id})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "折旧设置-删除")

    @allure.story("资产管理")
    @allure.title("折旧设置-列表筛选")
    def test_assert_depreciation_filtrate(self, login):
        #获取方案名称
        res1 = login.IlogAssetModule.api("资产管理", "折旧设置-列表").response(login_user="user2",cached=False)
        name = res1.json().get('data').get('content')[0].get('nickName')
        #方案列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "折旧设置-列表筛选").response(login_user="user2",cached=False,Template_values={"name": name})











#资产移动端相关内容
    #资产验收相关内容

    @allure.story("资产管理")
    @allure.title("移动端-资产验收-新增验收")
    def test_appacceptanceInfo_add(self, login):
        #获取采购单id
        res1 = login.IlogAssetModule.api("资产管理", "资产验收-选择采购单列表").response(login_user="user2", cached=False)
        cgid = res1.json().get('data').get('content')[0].get('id')
        #获取验收资产信息
        res2 = login.IlogAssetModule.api("资产管理", "资产验收-选择物资列表").response(login_user="user2", Template_values={"cgid": cgid})
        contactOrderCount = int(res2.json().get('data').get('materialVos')[0].get('contactOrderCount'))
        procureUnit = res2.json().get('data').get('materialVos')[0].get('procureUnit')
        procureUnitName = res2.json().get('data').get('materialVos')[0].get('procureUnitName')
        procurePrice = res2.json().get('data').get('materialVos')[0].get('procurePrice')
        materialId = res2.json().get('data').get('materialVos')[0].get('materialId')
        fkid = res2.json().get('data').get('materialVos')[0].get('id')
        procureId = res2.json().get('data').get('materialVos')[0].get('procureId')
        procureNo = res2.json().get('data').get('materialVos')[0].get('procureNo')
        checkCount = int(res2.json().get('data').get('materialVos')[0].get('checkCount'))
        materialName = res2.json().get('data').get('materialVos')[0].get('materialName')
        supplierId = res2.json().get('data').get('materialVos')[0].get('supplierId')
        supplierName = res2.json().get('data').get('materialVos')[0].get('supplierName')
        #新增购入验收
        keys = {
                "contactOrderCount":contactOrderCount,
                "procureUnit":procureUnit,
                "procureUnitName":procureUnitName,
                "procurePrice":procurePrice,
                "materialId":materialId,
                "fkid":fkid,
                "procureId":procureId,
                "procureNo":procureNo,
                "checkCount":checkCount,
                "materialName":materialName,
                "supplierId":supplierId,
                "supplierName":supplierName
                }
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产验收-新增购入验收").response(login_user="user2", Template_values=keys)
        #其他方式登记验收
        source = ["LEASE","DONATION","PROBATION","SELF"]
        for sourcetype in source:

            #获取计量单位信息
            res3 = login.IlogAssetModule.api("资产管理", "资产验收-计量单位列表").response(login_user="user2", cached=False)
            unitname = res3.json().get('data')[0].get('nickName')
            unitid = res3.json().get('data')[0].get('id')
            #发起新增验收
            d2 = login.IlogAssetModule.api("资产管理", "移动端-资产验收-新增其他方式验收").response(login_user="user2", Template_values={"unitid": unitid,"unitname":unitname,"sourcetype":sourcetype})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产验收-新增其他方式验收")

    @allure.story("资产管理")
    @allure.title("移动端-资产验收-验收列表筛选")
    def test_appassert_acceptanceInfo_filtrate(self, login):
        # 获取验收单号
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产验收-验收列表").response(login_user="user2", cached=False)
        #获取验收单号
        orderNumber = res1.json().get('data').get('content')[0].get('code')
        #验收列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产验收-验收列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("移动端-资产验收-验收单详情")
    def test_appassert_acceptanceInfo_detail(self, login):
        #获取验收单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产验收-验收列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看验收详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产验收-验收单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产验收-验收单详情")

    @allure.story("资产管理")
    @allure.title("移动端-资产档案-直接登记")
    def test_appassert_add(self, login):
    #直接登记购入
        #获取资产分类
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-查看资产分类").response(login_user="user2", cached=False)
        assettype = res1.json().get('data')[0].get('id')
        assettypename = res1.json().get('data')[0].get('nickName')
        #获取位置信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-资产位置选择列表").response(login_user="user2", cached=False)
        areaid = res2.json().get('data')[0].get('id')
        areanickname = res2.json().get('data')[0].get('nickName')
        #获取负责人信息
        res3 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res3.json().get('data').get('content')[0].get('id')
        username = res3.json().get('data').get('content')[0].get('nickName')
        #获取供应商信息
        res4 = login.IlogAssetModule.api("资产管理", "资产档案-供应商列表").response(login_user="user2", cached=False)
        companyid = res4.json().get('data').get('content')[0].get('id')
        companyname = res4.json().get('data').get('content')[0].get('companyName')
        #入库时间
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        #发起直接登记购入请求
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-直接登记购入").response(login_user="user2",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username,"companyid": companyid,"companyname": companyname})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产档案-直接登记购入")
    #直接登记自研自建
        d2 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-直接登记自研自建").response(login_user="user2",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username,"companyid": companyid,"companyname": companyname})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d2, "资产管理", "移动端-资产档案-直接登记自研自建")
    #直接登记租赁
        d3 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-直接登记租赁").response(login_user="user1",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d3, "资产管理", "移动端-资产档案-直接登记租赁")
    #直接登记试用
        d4 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-直接登记试用").response(login_user="user1",
         Template_values={"assettype": assettype,"assettypename": assettypename,"date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                          "userid": userid,"username": username})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d4, "资产管理", "移动端-资产档案-直接登记试用")
    #直接登记捐赠
        d5 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-直接登记捐赠").response(login_user="user1",
        Template_values={"assettype": assettype, "assettypename": assettypename, "date_time": date_time,"areaid": areaid,"areanickname": areanickname,
                         "userid": userid,"username": username})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d5, "资产管理", "移动端-资产档案-直接登记捐赠")



    @allure.story("资产管理")
    @allure.title("资产档案-移动端-资产列表筛选")
    def test_appassertlist_filtrate(self, login):
        # 获取资产code
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-资产列表").response(login_user="user2", cached=False)
        assetcode = res1.json().get('data').get('content')[0].get('code')
        # 资产列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-资产列表筛选").response(login_user="user2", Template_values={"assetcode": assetcode})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产档案-资产列表筛选")


    @allure.story("资产管理")
    @allure.title("资产档案-移动端-资产详情")
    def test_appassertlist_detail(self, login):
        # 获取资产id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-资产列表").response(login_user="user2", cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产档案-资产详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产档案-资产详情")




    # 资产领用相关内容
    @allure.story("资产管理")
    @allure.title("移动端-资产领用-新增领用")
    def test_appassert_receive_add(self, login):
        # 获取领用资产
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产领用-获取领用资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #获取领用人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        #新增资产领用
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产领用-新增领用").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,"department":department,"departmentid":departmentid})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产领用-新增领用")


    @allure.story("资产管理")
    @allure.title("移动端-资产领用-领用列表筛选")
    def test_appassert_receive_filtrate(self, login):
        # 获取领用人信息
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res1.json().get('data').get('content')[0].get('id')
        #领用列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产领用-领用列表筛选").response(login_user="user2", Template_values={"userid": userid})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产领用-领用列表筛选")

    @allure.story("资产管理")
    @allure.title("移动端-资产领用-领用单详情")
    def test_appassert_receive_detail(self, login):
        #获取领用单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产领用-领用列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看领用详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产领用-领用单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产领用-领用单详情")



    # 资产借用相关内容
    @allure.story("资产管理")
    @allure.title("移动端-资产借用-新增借用")
    def test_appassert_borrow_add(self, login):
        # 获取借用人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        # 获取借用资产
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产领用-获取领用资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #归还时间
        now  = datetime.now().date()
        #新增资产借用
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产借用-新增借用").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,
                                "department":department,"departmentid":departmentid,"date":now})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产借用-新增借用")



    @allure.story("资产管理")
    @allure.title("移动端-资产借用-借用列表筛选")
    def test_appassert_borrow_filtrate(self, login):
        # 获取借用单号
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产借用-借用列表").response(login_user="user2", cached=False)
        #获取借用单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #借用列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产借用-借用列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)


    @allure.story("资产管理")
    @allure.title("移动端-资产借用-借用单详情")
    def test_appassert_borrow_detail(self, login):
        #获取借用单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产借用-借用列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看借用详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产借用-借用单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产借用-借用单详情")


    # 资产退还相关内容
    @allure.story("资产管理")
    @allure.title("移动端-资产退还-新增退还")
    def test_appassert_refund_add(self, login):
        # 获取退还资产
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产退还-获取退还资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #获取退还人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        # #新增资产退还
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产退还-新增退还").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,"department":department,"departmentid":departmentid})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产退还-新增退还")



    @allure.story("资产管理")
    @allure.title("移动端-资产退还-退还列表筛选")
    def test_appassert_refund_filtrate(self, login):
        # 获取退还单号
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产退还-退还列表").response(login_user="user2", cached=False)
        #获取退还单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #退还列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产退还-退还列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("移动端-资产退还-退还单详情")
    def test_appassert_refund_detail(self, login):
        #获取退还单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产退还-退还列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看退还详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产退还-退还单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产退还-退还单详情")




    # 资产归还相关内容
    @allure.story("资产管理")
    @allure.title("移动端-资产归还-新增归还")
    def test_appassert_restitution_add(self, login):
        # 获取归还资产
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产归还-获取归还资产").response(login_user="user2", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        #获取归还人信息
        res2 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res2.json().get('data').get('content')[0].get('id')
        username = res2.json().get('data').get('content')[0].get('nickName')
        department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        # #新增资产归还
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产归还-新增归还").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,"department":department,"departmentid":departmentid})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产归还-新增归还")



    @allure.story("资产管理")
    @allure.title("移动端-资产归还-归还列表筛选")
    def test_appassert_restitution_filtrate(self, login):
        # 获取归还单号
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产归还-归还列表").response(login_user="user2", cached=False)
        #获取归还单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #归还列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产归还-归还列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("移动端-资产归还-归还单详情")
    def test_appassert_restitution_detail(self, login):
        #获取归还单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产归还-归还列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看归还详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产归还-归还单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产归还-归还单详情")


    # 资产调拨相关内容
    @allure.story("资产管理")
    @allure.title("移动端-资产调拨-新增调拨")
    def test_appassert_allocation_add(self, login):
        # 获取位置信息
        res1 = login.IlogAssetModule.api("资产管理", "资产档案-资产位置选择列表").response(login_user="user2", cached=False)
        areaid1 = res1.json().get('data')[0].get('id')
        areanickname1 = res1.json().get('data')[0].get('nickName')
        areaid2 = res1.json().get('data')[1].get('id')
        areanickname2 = res1.json().get('data')[1].get('nickName')
        #获取资产信息
        res2 = login.IlogAssetModule.api("资产管理", "移动端-资产调拨-获取调拨资产").response(login_user="user2", cached=False,Template_values={ "areaid1": areaid1})
        assetid = res2.json().get('data').get('content')[0].get('id')
        assetcode = res2.json().get('data').get('content')[0].get('code')
        assetnickName = res2.json().get('data').get('content')[0].get('nickName')
        assetType = res2.json().get('data').get('content')[0].get('assetType')
        assetTypeName = res2.json().get('data').get('content')[0].get('assetTypeName')
        #获取人员信息
        res3 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid = res3.json().get('data').get('content')[0].get('id')
        username = res3.json().get('data').get('content')[0].get('nickName')
        department = res3.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid = res3.json().get('data').get('content')[0].get('departs')[0].get('id')
        #新增资产调拨
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产调拨-新增调拨").response(login_user="user2",
              Template_values={ "assetid": assetid,"assetcode":assetcode,"assetnickName":assetnickName,"userid":userid,"username":username,
                                "department":department,"departmentid":departmentid,"areaid1":areaid1,"areanickname1":areanickname1,"areaid2":areaid2,"areanickname2":areanickname2})


    @allure.story("资产管理")
    @allure.title("移动端-资产调拨-调拨列表筛选")
    def test_appassert_allocation_filtrate(self, login):
        # 获取调拨单号
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产调拨-调拨列表").response(login_user="user2", cached=False)
        #获取调拨单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #调拨列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产调拨-调拨列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("移动端-资产调拨-调拨单详情")
    def test_appassert_restitution_detail(self, login):
        #获取调拨单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产调拨-调拨列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看调拨详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产调拨-调拨单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产调拨-调拨单详情")





    # 资产交接相关内容
    @allure.story("资产管理")
    @allure.title("移动端-资产交接-交接单详情")
    def test_appassert_handover_add(self, login):
        # 获取交接资产
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产交接-获取交接资产").response(login_user="user", cached=False)
        assetid = res1.json().get('data').get('content')[0].get('id')
        assetcode = res1.json().get('data').get('content')[0].get('code')
        assetnickName = res1.json().get('data').get('content')[0].get('nickName')
        # 获取被交接人信息
        res2 = login.IlogAssetModule.api("资产管理", "移动端-资产交接-交接人列表").response(login_user="user2", cached=False)
        userid2 = res2.json().get('data').get('content')[0].get('id')
        username2 = res2.json().get('data').get('content')[0].get('nickName')
        department2 = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid2 = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
        # 获取交际人信息
        res3 = login.IlogAssetModule.api("资产管理", "资产档案-负责人列表").response(login_user="user2", cached=False)
        userid1 = res3.json().get('data').get('content')[0].get('id')
        username1 = res3.json().get('data').get('content')[0].get('nickName')
        department1 = res3.json().get('data').get('content')[0].get('departs')[0].get('nickName')
        departmentid1 = res3.json().get('data').get('content')[0].get('departs')[0].get('id')
        # 新增交接
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产交接-新增交接").response(login_user="user2",
         Template_values={"assetid": assetid, "assetcode": assetcode,"assetnickName": assetnickName, "userid1": userid1,"username1": username1,"department1": department1,
                          "departmentid1": departmentid1,"userid2": userid2,"username2": username2,"department2": department2,
                          "departmentid2": departmentid2})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产交接-新增交接")


    @allure.story("资产管理")
    @allure.title("移动端-资产交接-交接列表筛选")
    def test_appassert_allocation_filtrate(self, login):
        # 获取交接单号
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产交接-交接列表").response(login_user="user2", cached=False)
        # 获取交接单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        # 交接列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产交接-交接列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("移动端-资产交接-交接单详情")
    def test_appassert_restitution_detail(self, login):
        # 获取交接单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产交接-交接列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        # 查看交接详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产交接-交接单详情").response(login_user="user2", Template_values={"id": id})
        # 断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产交接-交接单详情")





    #资产处理相关内容
    @allure.story("资产管理")
    @allure.title("移动端-资产处置-新增处置")
    def test_appassert_dispose_add(self, login):
        #处置类型
        dispositionType = ['SCRAP','SELL','DONATION','RENTING_TERMINATION']

        for distype in dispositionType:
            #获取处置资产
            res1 = login.IlogAssetModule.api("资产管理", "移动端-资产处置-获取处置资产").response(login_user="user2", Template_values={"distype": distype})
            assetid = res1.json().get('data').get('content')[0].get('id')
            assetcode = res1.json().get('data').get('content')[0].get('code')
            assetnickName = res1.json().get('data').get('content')[0].get('nickName')
            price = res1.json().get('data').get('content')[0].get('price')
            netValue = res1.json().get('data').get('content')[0].get('netValue')
            #获取处置人信息
            res2 = login.IlogAssetModule.api("资产管理", "移动端-资产处置-处置人列表").response(login_user="user2", cached=False)
            userid = res2.json().get('data').get('content')[0].get('id')
            username = res2.json().get('data').get('content')[0].get('nickName')
            department = res2.json().get('data').get('content')[0].get('departs')[0].get('nickName')
            departmentid = res2.json().get('data').get('content')[0].get('departs')[0].get('id')
            #新增资产处置
            d1 = login.IlogAssetModule.api("资产管理", "移动端-资产处置-新增处置").response(login_user="user2",
             Template_values={"assetid": assetid, "assetcode": assetcode,"assetnickName": assetnickName, "userid": userid,"username": username,"department": department,
                              "departmentid": departmentid,"price": price,"netValue":netValue,"distype": distype})
            # 断言
            login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产处置-新增处置")



    @allure.story("资产管理")
    @allure.title("移动端-资产处置-处置列表筛选")
    def test_appassert_dispose_filtrate(self, login):
        # 获取处置单号
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产处置-处置列表").response(login_user="user2", cached=False)
        #获取处置单号
        orderNumber = res1.json().get('data').get('content')[0].get('orderNumber')
        #处置列表筛选
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产处置-处置列表筛选").response(login_user="user2", Template_values={"orderNumber": orderNumber})
        # 断言返回的数据是搜索的数据
        login.IlogAssetModule.asset_filtrate_assert(d1,orderNumber)

    @allure.story("资产管理")
    @allure.title("移动端-资产处置-处置单详情")
    def test_appassert_dispose_detail(self, login):
        #获取处置单id
        res1 = login.IlogAssetModule.api("资产管理", "移动端-资产处置-处置列表").response(login_user="user2",cached=False)
        id = res1.json().get('data').get('content')[0].get('id')
        #查看处置详情
        d1 = login.IlogAssetModule.api("资产管理", "移动端-资产处置-处置单详情").response(login_user="user2", Template_values={"id": id})
        #断言
        login.IlogAssetModule.ilogasset_assert(d1, "资产管理", "移动端-资产处置-处置单详情")













if __name__ == '__main__':
    pytest.main(['-s', '--alluredir', r'D:\jiekou\fq_api_automation\temp'])
    allure_results_dir = r'D:\jiekou\fq_api_automation\temp'  # 源目录，pytest生成Allure结果数据的地方
    allure_report_dir = r'/report'  # 目标目录，你想要生成Allure报告的地方
    generate_report_cmd = ['allure', 'generate', allure_results_dir, '-o', allure_report_dir, '--clean']
    subprocess.run(generate_report_cmd, check=True)
    os.system('allure serve ../report')
