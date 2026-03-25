import os.path
from imp import find_module
from pipes import Template

from IR.base_requests import BaseRequest
from public.get_api_msg import get_api_detail_msg

from config.setting import data_file_root_path
from utils.assert_util import AssertUtil

class IlogTransportModule(BaseRequest):
    """
    功能特性模块--命名方式必须已Module结尾
    """

    def __init__(self, access_token,access_token2,access_token3,access_token4,access_token5):
        super().__init__(access_token,access_token2,access_token3,access_token4,access_token5)
        self.data_module_path=os.path.join(data_file_root_path,os.path.basename(os.path.abspath(os.path.join(__file__, os.pardir)) ))
        self.file_name="方顷接口.csv"
        self.assert_util=AssertUtil()

    def api(self, module_name, tips):
        self.request_target = get_api_detail_msg(module_name=module_name, tips=tips,data_module_path=self.data_module_path,file_name=self.file_name)
        self.step = self.request_target.get('Tips', '无接口说明')
        return self

    def ilogtransport_assert(self,res,module_name,tips):
        """
        常规的断言
        :param res:
        :param module_name:
        :param tips:
        :return:
        """
        data_module_path=self.data_module_path
        file_name=self.file_name
        self.request_target = get_api_detail_msg(module_name=module_name, tips=tips,
                                                 data_module_path=self.data_module_path, file_name=self.file_name)
        return self.assert_util.assert_util(res,module_name,tips,data_module_path,file_name)
    #
    # def asset_filtrate_assert(self,res,orderNumber):
    #     orderNumber1 = res.json().get('data').get('content')[0].get('orderNumber')
    #     if orderNumber == orderNumber1:
    #         return True
    #
    # def asset_AssetLedgerList_assert(self,res,code):
    #     code1 = res.json().get('data').get('content').get('content')[0].get('code')
    #     if code == code1:
    #         return True








