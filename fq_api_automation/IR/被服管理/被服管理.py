import os.path
from imp import find_module
from pipes import Template

from IR.base_requests import BaseRequest
from public.get_api_msg import get_api_detail_msg

from config.setting import data_file_root_path
from utils.assert_util import AssertUtil

class IlogClothingModule(BaseRequest):
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

    def clothing_filtrate_assert(self,res,codeno):
        codeno1 = res.json().get('data').get('content')[0].get('orderNo')
        if codeno == codeno1:
            return True

    def clothing_detail_filtrate_assert(self,res,code):
        code1 = res.json().get('data').get('content')[0].get('code')
        if code == code1:
            return True