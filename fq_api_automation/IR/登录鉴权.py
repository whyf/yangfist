from IR.base_requests import BaseRequest
from config.configHandler import ConfigHandler

con=ConfigHandler()
class OauthModule(BaseRequest):
    """
    功能特性模块--命名方式必须已Module结尾
    """

    def __init__(self, ck):
        super().__init__(ck)


    def judge_get_token(self,res):
        """
        判断--是否能正常登录
        :param res:
        :return:
        """
        if res.json().get("access_token"):
            return True

