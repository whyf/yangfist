import os.path
from imp import find_module
from pipes import Template

from IR.base_requests import BaseRequest
from public.get_api_msg import get_api_detail_msg

from config.setting import data_file_root_path
from utils.assert_util import AssertUtil

class IotplatDeviceModule(BaseRequest):
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

    def iotplat_device_assert(self,res,module_name,tips):
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









    def judge_delete_protocol(self, res1,res2,id):
        """
        物联网-协议管理-删除协议是否成功
        :param data1:
        :param data2:
        :return:
        """
        msg=res1.json().get('msg')
        if msg=='success'  and  id not in [content.get('id') for content in res2.json().get('data').get('content')]:
            return True



    def judge_get_product_info(self,res,nickname):
        """
        物联网-产品—成功获取产品详情
        :param res:
        :param nickname:
        :return:
        """
        if  res.json().get('msg')=='success' and nickname == res.json().get('data').get('nickName'):
            return True


    def judge_delete_product(self, res,id):
        """
        物联网-协议管理-删除产品是否成功
        :param data1:
        :param data2:
        :return:
        """
        if   id not in [content.get('id') for content in res.json().get('data').get('content')]:
            return True


    def judge_get_device_info(self,res,nickname):
        """
        物联网-设备-判断设备详情展示是否正确
        :param res:
        :param nickname:
        :return:
        """
        if res.json().get('msg')=='success' and nickname ==res.json().get('data').get('nickName'):
            return True



    def judge_delete_device(self, res,id):
        """
        物联网-协议管理-删除协议是否成功
        :param data1:
        :param data2:
        :return:
        """

        if  id not in [content.get('id') for content in res.json().get('data').get('content')]:
            return True