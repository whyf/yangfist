"""
@author       : youfeng
@datetime     : 2024-09-23 16:03:38
@description  : 医废管理接口测试用例
"""

import allure
import random
from datetime import datetime
from requests import Response
from time import sleep
from pytest import fixture


@allure.epic("方顷科技智慧后勤")
@allure.feature("医废管理")
class TestCase:
    scrap_types = (
        "INFECT_SCRAP_TYPE",
        "INJURE_SCRAP_TYPE",
        "CHEMISTRY_SCRAP_TYPE",
        "MEDICINE_SCRAP_TYPE",
        "PATHOLOGY_SCRAP_TYPE",
        "LIFE_RUBBISH_TYPE",
    )

    @fixture(scope="module")
    def get_users_list(self, login):
        user_response: Response = login.ScrapModule.api(
            "用户管理", "人员管理-列表查询"
        ).response(login_user="user4")
        login.ScrapModule.assertion(user_response, "用户管理", "人员管理-列表查询")
        users: list = user_response.json()["data"]["content"]
        available_users = [user for user in users if user["defaultDepart"]]
        return available_users

    @fixture(scope="module")
    def get_supplier_list(self, login):
        supplier_response: Response = login.ScrapModule.api(
            "基础管理", "供应商管理-列表查询"
        ).response(login_user="user4")
        login.ScrapModule.assertion(
            supplier_response, "基础管理", "供应商管理-列表查询"
        )
        suppliers = supplier_response.json()["data"]["content"]
        return suppliers

    @allure.story("医废管理")
    @allure.title("流程：装袋-装箱-出库")
    def test_scrap_process(self, login, get_users_list, get_supplier_list):
        # 装袋补录
        scrap_type = random.choice(self.scrap_types)
        user1 = random.choice(get_users_list)
        user2 = random.choice(get_users_list)
        template_values = {
            "scrap_type": scrap_type,
            "operation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": f"{random.uniform(20,500):.2f}",
            "device_code": str(random.random())[2:10],
            "operator_id": user1["id"],
            "operator_name": user1["nickName"],
            "handover_person_id": user2["id"],
            "handover_person_name": user2["nickName"],
            "handover_person_dept_id": user2["defaultDepart"]["id"],
            "handover_person_dept_name": user2["defaultDepart"]["nickName"],
        }
        if scrap_type == "PATHOLOGY_SCRAP_TYPE":
            bag_response: Response = login.ScrapModule.api(
                "医废管理", "医废装袋-补录成功"
            ).response(
                login_user="user4",
                Template_values=template_values,
                body={
                    "wasteBaggedInfo": {
                        "patientName": "王刚",
                        "admissionNum": "5342424",
                        "pathologyType": "PLACENTA",
                        "operationName": "烂尾切除术",
                    },
                },
            )
        else:
            bag_response: Response = login.ScrapModule.api(
                "医废管理", "医废装袋-补录成功"
            ).response(login_user="user4", Template_values=template_values)
        login.ScrapModule.assertion(bag_response, "医废管理", "医废装袋-补录成功")
        bag_info = bag_response.json()["data"]

        # 装箱补录
        sleep(0.5)
        bag_id = bag_info["id"]
        template_values = {
            "scrap_type": scrap_type,
            "operation_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": f"{random.uniform(20,500):.2f}",
            "operator_id": user1["id"],
            "operator_name": user1["nickName"],
            "bag_id": bag_id,
        }

        packed_response: Response = login.ScrapModule.api(
            "医废管理", "医废装箱-补录成功"
        ).response(login_user="user4", Template_values=template_values)
        login.ScrapModule.assertion(packed_response, "医废管理", "医废装箱-补录成功")
        packed_info = packed_response.json()["data"]

        # 出库补录
        sleep(0.5)
        packed_id = packed_info["id"]
        supplier = random.choice(get_supplier_list)
        template_values = {
            "scrap_type": scrap_type,
            "outbound_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": f"{random.uniform(20,500):.2f}",
            "out_bound_person_id": user1["id"],
            "out_bound_person_name": user1["nickName"],
            "packed_id": packed_id,
            "recipient_id": supplier["id"],
            "recipient_name": supplier["nickName"],
        }

        out_bound_response: Response = login.ScrapModule.api(
            "医废管理", "医废出库-补录成功"
        ).response(login_user="user4", Template_values=template_values)
        login.ScrapModule.assertion(out_bound_response, "医废管理", "医废出库-补录成功")

    @allure.story("医废管理")
    @allure.title("医废装袋-列表查询")
    def test_get_scrap_bag_list(self, login):
        d1: Response = login.ScrapModule.api("医废管理", "医废装袋-列表查询").response(
            login_user="user4"
        )
        login.ScrapModule.assertion(d1, "医废管理", "医废装袋-列表查询")

    @allure.story("医废管理")
    @allure.title("医废装箱-列表查询")
    def test_get_scrap_packed_list(self, login):
        d1: Response = login.ScrapModule.api("医废管理", "医废装箱-列表查询").response(
            login_user="user4"
        )
        login.ScrapModule.assertion(d1, "医废管理", "医废装箱-列表查询")

    @allure.story("医废管理")
    @allure.title("医废出库-列表查询")
    def test_get_scrap_outbound_list(self, login):
        d1: Response = login.ScrapModule.api("医废管理", "医废出库-列表查询").response(
            login_user="user4"
        )
        login.ScrapModule.assertion(d1, "医废管理", "医废出库-列表查询")

    @allure.story("医废管理")
    @allure.title("医废出库-出库单列表、详情")
    def test_get_scrap_outbound_details(self, login):
        # 医废出库-列表查询
        d1: Response = login.ScrapModule.api("医废管理", "医废出库-列表查询").response(
            login_user="user4"
        )
        login.ScrapModule.assertion(d1, "医废管理", "医废出库-列表查询")

        # 医废出库-出库单详情
        outbound_info = d1.json()["data"]["content"][0]
        outbound_id = outbound_info["id"]
        d2: Response = login.ScrapModule.api(
            "医废管理", "医废出库-出库单详情"
        ).response(login_user="user4", Template_values={"outbound_id": outbound_id})
        login.ScrapModule.assertion(d2, "医废管理", "医废出库-出库单详情")

    @allure.story("医废管理")
    @allure.title("医废溯源-医废袋/箱详情")
    def test_get_scrap_traceability(self, login):
        # 医废装袋-列表查询
        bag_response: Response = login.ScrapModule.api(
            "医废管理", "医废装袋-列表查询"
        ).response(login_user="user4")
        login.ScrapModule.assertion(bag_response, "医废管理", "医废装袋-列表查询")
        # 医废装箱-列表查询
        packed_response: Response = login.ScrapModule.api(
            "医废管理", "医废装箱-列表查询"
        ).response(login_user="user4")
        login.ScrapModule.assertion(packed_response, "医废管理", "医废装箱-列表查询")

        # 医废袋详情
        bagsCode = bag_response.json()["data"]["content"][0]["bagsCode"]
        boxCode = packed_response.json()["data"]["content"][0]["boxCode"]
        d1: Response = login.ScrapModule.api(
            "医废管理", "医废溯源-医废袋/箱详情"
        ).response(login_user="user4", Template_values={"code": bagsCode})
        login.ScrapModule.assertion(d1, "医废管理", "医废溯源-医废袋/箱详情")
        # 医废箱详情
        d2: Response = login.ScrapModule.api(
            "医废管理", "医废溯源-医废袋/箱详情"
        ).response(Template_values={"code": boxCode})
        login.ScrapModule.assertion(d2, "医废管理", "医废溯源-医废袋/箱详情")

    @allure.story("医废管理")
    @allure.title("医废库存-医废袋统计")
    def test_get_scrap_bags_count(self, login):
        d1: Response = login.ScrapModule.api(
            "医废管理", "医废库存-医废袋统计"
        ).response(login_user="user4")
        login.ScrapModule.assertion(d1, "医废管理", "医废库存-医废袋统计")

    @allure.story("医废管理")
    @allure.title("医废库存-医废袋列表、详情")
    def test_get_scrap_bags_details(self, login):
        # 医废库存-医废袋列表查询
        d1: Response = login.ScrapModule.api(
            "医废管理", "医废库存-医废袋列表查询"
        ).response(login_user="user4")
        login.ScrapModule.assertion(d1, "医废管理", "医废库存-医废袋列表查询")
        inventory_bag_info = d1.json()["data"]["content"][0]
        bag_id = inventory_bag_info["id"]

        # 医废库存-医废袋详情
        d2: Response = login.ScrapModule.api(
            "医废管理", "医废库存-医废袋详情"
        ).response(login_user="user4", Template_values={"bag_id": bag_id})
        login.ScrapModule.assertion(d2, "医废管理", "医废库存-医废袋详情")

    @allure.story("医废管理")
    @allure.title("医废库存-医废箱统计")
    def test_get_scrap_packed_count(self, login):
        d1: Response = login.ScrapModule.api(
            "医废管理", "医废库存-医废箱统计"
        ).response(login_user="user4")
        login.ScrapModule.assertion(d1, "医废管理", "医废库存-医废箱统计")

    @allure.story("医废管理")
    @allure.title("医废库存-医废箱列表、详情")
    def test_get_scrap_packed_details(self, login):
        # 医废库存-医废箱列表查询
        d1: Response = login.ScrapModule.api(
            "医废管理", "医废库存-医废箱列表查询"
        ).response(login_user="user4")
        login.ScrapModule.assertion(d1, "医废管理", "医废库存-医废箱列表查询")

        # 医废库存-医废箱详情
        inventory_packed_info = d1.json()["data"]["content"][0]
        packed_id = inventory_packed_info["id"]
        d2: Response = login.ScrapModule.api(
            "医废管理", "医废库存-医废箱详情"
        ).response(login_user="user4", Template_values={"packed_id": packed_id})
        login.ScrapModule.assertion(d2, "医废管理", "医废库存-医废箱详情")

    @allure.story("医废管理")
    @allure.title("PAD-装袋、装箱、出库流程")
    def test_pad_scrap_process(self, login, get_users_list, get_supplier_list):
        # 新增未签收的医废袋
        scrap_type = random.choice(self.scrap_types)
        user1 = random.choice(get_users_list)
        user2 = random.choice(get_users_list)
        template_values = {
            "scrap_type": scrap_type,
            "weight": f"{random.uniform(20,500):.2f}",
            "device_code": str(random.random())[2:10],
            "operator_id": user1["id"],
            "operator_name": user1["nickName"],
        }
        if scrap_type == "PATHOLOGY_SCRAP_TYPE":
            d1: Response = login.ScrapModule.api("医废管理", "PAD-新增医废袋").response(
                login_user="user4",
                Template_values=template_values,
                body={
                    "wasteBaggedInfo": {
                        "patientName": "王刚",
                        "admissionNum": "5342424",
                        "pathologyType": "PLACENTA",
                        "operationName": "烂尾切除术",
                    },
                },
            )
        else:
            d1: Response = login.ScrapModule.api("医废管理", "PAD-新增医废袋").response(
                login_user="user4", Template_values=template_values
            )
        # 断言
        login.ScrapModule.assertion(d1, "医废管理", "PAD-新增医废袋")
        pad_bag_data = d1.json()["data"]
        bag_id = pad_bag_data["id"]

        # PAD-医废袋交接签名
        d2: Response = login.ScrapModule.api("医废管理", "PAD-医废袋交接签名").response(
            login_user="user4",
            Template_values={
                "bag_id": bag_id,
                "handover_person_id": user2["id"],
                "handover_person_name": user2["nickName"],
                "handover_person_dept_id": user2["defaultDepart"]["id"],
                "handover_person_dept_name": user2["defaultDepart"]["nickName"],
            },
        )
        login.ScrapModule.assertion(d2, "医废管理", "PAD-医废袋交接签名")

        # PAD-新增医废箱
        sleep(0.5)
        bag_id = pad_bag_data["id"]
        template_values = {
            "scrap_type": scrap_type,
            "weight": f"{random.uniform(20,500):.2f}",
            "operator_id": user1["id"],
            "operator_name": user1["nickName"],
            "bag_id": bag_id,
        }

        d3: Response = login.ScrapModule.api("医废管理", "PAD-新增医废箱").response(
            login_user="user4", Template_values=template_values
        )
        # 断言
        login.ScrapModule.assertion(d3, "医废管理", "PAD-新增医废箱")
        pad_packed_data = d3.json()["data"]

        # PAD-医废出库
        sleep(0.5)
        packed_id = pad_packed_data["id"]
        supplier = random.choice(get_supplier_list)
        template_values = {
            "weight": f"{random.uniform(20,500):.2f}",
            "out_bound_person_id": user1["id"],
            "out_bound_person_name": user1["nickName"],
            "packed_id": packed_id,
            "recipient_id": supplier["id"],
            "recipient_name": supplier["nickName"],
        }

        d4: Response = login.ScrapModule.api("医废管理", "PAD-医废出库").response(
            login_user="user4", Template_values=template_values
        )
        login.ScrapModule.assertion(d4, "医废管理", "PAD-医废出库")
        outbound_id = d4.json()["data"]["id"]

        # PAD-医废出库交接签名
        d5: Response = login.ScrapModule.api(
            "医废管理", "PAD-医废出库交接签名"
        ).response(login_user="user4", Template_values={"outbound_id": outbound_id})
        login.ScrapModule.assertion(d5, "医废管理", "PAD-医废出库交接签名")

    @allure.story("医废管理")
    @allure.title("PAD-本车库存数据统计")
    def test_get_scrap_car_count(self, login):
        d1: Response = login.ScrapModule.api(
            "医废管理", "PAD-本车库存数据统计"
        ).response(login_user="user4")
        login.ScrapModule.assertion(d1, "医废管理", "PAD-本车库存数据统计")

    @allure.story("医废管理")
    @allure.title("PAD-本车库存列表查询")
    def test_get_scrap_car_list(self, login):
        d1: Response = login.ScrapModule.api(
            "医废管理", "PAD-本车库存列表查询"
        ).response(login_user="user4")
        login.ScrapModule.assertion(d1, "医废管理", "PAD-本车库存列表查询")

    @allure.story("医废管理")
    @allure.title("PAD-医废概况")
    def test_get_scrap_statistic_summarize(self, login):
        d1: Response = login.ScrapModule.api("医废管理", "PAD-医废概况").response(
            login_user="user4"
        )
        login.ScrapModule.assertion(d1, "医废管理", "PAD-医废概况")

    @allure.story("医废管理")
    @allure.title("PAD-医废占比")
    def test_get_scrap_statistic_ratio(self, login):
        d1: Response = login.ScrapModule.api("医废管理", "PAD-医废占比").response(
            login_user="user4"
        )
        login.ScrapModule.assertion(d1, "医废管理", "PAD-医废占比")

    @allure.story("医废管理")
    @allure.title("PAD-医废统计")
    def test_get_scrap_statistic(self, login):
        d1: Response = login.ScrapModule.api("医废管理", "PAD-医废统计").response(
            login_user="user4"
        )
        login.ScrapModule.assertion(d1, "医废管理", "PAD-医废统计")
