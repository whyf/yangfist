import os.path
import demjson3
import pandas as pd
from cachetools import TTLCache, cached
from IR.base_requests import BaseRequest
from config.setting import data_file_root_path
from config.logHandler import exception_decorator
from utils.assert_util import AssertUtil
from string import Template


class ScrapModule(BaseRequest):
    """
    功能特性模块--命名方式必须已Module结尾
    """

    def __init__(
        self, access_token, access_token2, access_token3, access_token4, access_token5
    ):
        super().__init__(
            access_token, access_token2, access_token3, access_token4, access_token5
        )
        self.data_module_path = os.path.join(
            data_file_root_path,
            os.path.basename(os.path.abspath(os.path.join(__file__, os.pardir))),
        )
        self.file_name = "医废管理.csv"

    @cached(TTLCache(maxsize=100, ttl=100))
    def get_csv(self, module_name, file_name):
        csv_path = os.path.join(data_file_root_path, module_name, file_name)
        csv = pd.read_csv(csv_path, encoding="gbk")
        print(
            f"行列数：{csv.shape},请确认没有空行，有空行请删除",
        )
        csv["接口参数"] = csv["接口参数"].astype("str").str.replace("True", "true")
        # 请求头和请求参数为空的替换成空字典
        csv["接口参数"] = csv["接口参数"].apply(
            lambda x: "{}" if pd.isna(x) or x == "nan" or x.isspace() else x
        )
        csv["请求头"] = csv["请求头"].apply(
            lambda x: "{}" if pd.isna(x) or x == "" or x.isspace() else x
        )
        csv["预期结果"] = csv["预期结果"].astype("str").str.replace("TRUE", "True")
        try:
            for index, i in enumerate(csv["接口参数"]):
                demjson3.decode(i)
        except Exception:
            print("接口参数可能有问题,详细如下，或有空白行")
            print("问题行数：", index + 2)
            print(i)
        return csv

    def get_api_detail_msg(self, data_module_path, file_name, module_name, tips):
        """

        :param module_name: excel中的模块名
        :param tips: 接口描述
        :return:
        """
        df = self.get_csv(data_module_path, file_name)
        row = df.loc[(df["模块名"] == module_name) & (df["接口描述"] == tips)]
        if len(row) > 1:
            print(f"{module_name}  {tips} 出现重复数据，请手动处理，这里只取第一个数据")
        try:
            row_dict = row.iloc[0].to_dict()
            dic = {
                "Url": row_dict.get("接口地址"),
                "Scheme": row_dict.get("Scheme"),
                "Method": row_dict.get("请求方式"),
                "Data": row_dict.get("接口参数"),
                "Header": row_dict.get("请求头"),
                "Tips": row_dict.get("接口描述"),
                "ModuleName": row_dict.get("模块名"),
                "validate_value": row_dict.get("校验字段"),
                "chick_type": row_dict.get("校验方式"),
                "expected_value": row_dict.get("预期结果"),
            }
            return dic
        except IndexError:
            print(f"excel中 没有找到 {module_name}, {tips}  的数据")
            raise IndexError

    def api(self, module_name, tips):
        self.request_target = self.get_api_detail_msg(
            module_name=module_name,
            tips=tips,
            data_module_path=self.data_module_path,
            file_name=self.file_name,
        )
        self.step = self.request_target.get("Tips", "无接口说明")
        return self

    @exception_decorator()
    def response(self, *args, **kwargs) -> any:
        """
        Template_values:传入替换的参数，在你的excel中 以${xxx}作为占位符的可以进行替换 ->dict
        body:可替换data参数   ->dict
        cached:是否命中缓存 bool值  默认开启
        :param args:
        :param kwargs:
        :return:
        """
        # 动态参数

        Template_values = kwargs.get("Template_values")
        body = kwargs.get("body")
        header = kwargs.get("header")
        cached = kwargs.get("cached")  # 是否走缓存
        login_user = kwargs.get("login_user")  # 使用哪个登录用户
        if Template_values:
            self.request_target["Url"] = Template(
                self.request_target["Url"]
            ).safe_substitute(Template_values)
        if self.request_target["Data"]:
            self.request_target["Data"] = Template(
                self.request_target["Data"]
            ).safe_substitute(Template_values)
        if self.request_target["Header"]:
            self.request_target["Header"] = Template(
                self.request_target["Header"]
            ).safe_substitute(Template_values)
        self.request_target["Data"] = demjson3.decode(self.request_target["Data"])
        self.request_target["Header"] = demjson3.decode(self.request_target["Header"])
        if isinstance(body, dict):
            self.request_target["Data"].update(body)
        if isinstance(header, dict):
            self.request_target["Header"].update(header)  
        r = self.get_response(self.request_target, cached, login_user)
        return r

    def assert_util(self, res, module_name, tips, data_module_path, file_name):
        assert_util = AssertUtil()
        request_target = self.get_api_detail_msg(
            module_name=module_name,
            tips=tips,
            data_module_path=data_module_path,
            file_name=file_name,
        )
        validate_value = request_target["validate_value"]
        chick_type = request_target["chick_type"]
        expected_value = request_target["expected_value"]
        actually_value = assert_util.extract_by_jsonpath(
            res.json(), extract_expression=f"$..{validate_value}"
        )
        assert_util.validate_response(actually_value, expected_value, chick_type)

    def assertion(self, res, module_name, tips):
        """
        常规的断言
        :param res:
        :param module_name:
        :param tips:
        :return:
        """
        data_module_path = self.data_module_path
        file_name = self.file_name
        return self.assert_util(res, module_name, tips, data_module_path, file_name)

