from urllib.parse import urljoin
import allure
import os, json
import requests
from config.logHandler import exception_decorator
from utils.webRequest import WebRequest
from config.configHandler import ConfigHandler
from cachetools import TTLCache
from string import Template
from public.get_api_msg import get_api_detail_msg
import functools
import traceback
path = os.path.dirname(__file__)
conf = ConfigHandler()
import demjson3

def decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if func.__name__.startswith("judge_"):
            msg = '断言：' + func.__doc__
            with allure.step('{oper}'.format(oper=msg)):
                pass
        try:
            return func(*args, **kwargs)
        except Exception as e:
            fail_msg = f"函数{func.__module__}.{func.__name__}执行"
            with allure.step('步骤 ERROR：{oper} 失败'.format(oper=fail_msg)):
                allure.attach(str(args), "*args")
                allure.attach(str(kwargs), "**kwargs")
                extra = {
                    'extra_method':func.__name__,
                    'extra_module':func.__module__,
                }
                #traceback.format_exc()表示哪行代码的错误
                allure.attach('ERROR:message:{0},traceback:{1}'.format(str(e),traceback.format_exc()),"ERROR")
            raise e

    return wrapper

cache = (TTLCache(maxsize=1000, ttl=1800))

class BaseRequest():

    def __init__(self, access_token,access_token2,access_token3,access_token4,access_token5):
        self.access_token = access_token
        self.access_token2=access_token2
        self.access_token3=access_token3
        self.access_token4=access_token4
        self.access_token5=access_token5
        self._dict = object.__getattribute__(self, '__dict__')
        self.step = None


    def __getattribute__(self, attr):
        """
        拦截属性访问
        :param attr:
        :return:
        """
        if attr.startswith('api'):
            return object.__getattribute__(self, attr)
        else:
            obj = object.__getattribute__(self, attr)
            if callable(obj):
                return decorator(obj)
            else:
                return obj

    def api(self,data_module_path,file_name,module_name, tips):

        self.request_target = get_api_detail_msg(data_module_path,file_name,module_name, tips)
        self.step = self.request_target.get('Tips', '无接口说明')
        return self

    @exception_decorator()
    def response(self,*args,**kwargs) -> any:
        """
        Template_values:传入替换的参数，在你的excel中 以${xxx}作为占位符的可以进行替换 ->dict
        body:可替换data参数   ->dict
        cached:是否命中缓存 bool值  默认开启
        :param args:
        :param kwargs:
        :return:
        """
        #动态参数

        Template_values = kwargs.get("Template_values")
        body = kwargs.get("body")
        header = kwargs.get("header")
        cached = kwargs.get("cached") #是否走缓存
        login_user = kwargs.get("login_user") #使用哪个登录用户
        if Template_values:
            self.request_target['Url'] = Template(self.request_target['Url']).safe_substitute(Template_values)
            if self.request_target['Data']:
                self.request_target['Data'] = Template(self.request_target['Data']).safe_substitute(Template_values)
            if self.request_target['Header']:
                self.request_target['Header'] = Template(self.request_target['Header']).safe_substitute(Template_values)
        self.request_target['Data'] = demjson3.decode(self.request_target['Data'])
        self.request_target['Header'] = demjson3.decode(self.request_target['Header'])
        if isinstance(body, dict):
            self.request_target['Data'].update(body)
        if isinstance(header, dict):
            self.request_target['Header'].update(header)
        r = self.get_response(self.request_target,cached,login_user)
        return r


    def get_response(self, data,cached,login_user) -> requests.Response:
        # 缓存
        data_str = str(sorted(data.items()))
        if cached is not False:#特殊情况不走缓存
            if (data_str) in cache:
                return cache[(data_str)]
        response = self.send_method(data,login_user)
        cache[(data_str)] = response
        return response

    def send_method(self, data,login_user=None) -> requests.Response:
        _url, _scheme, _method, _data, _headers = data.get("Url"), data.get("Scheme"), data.get("Method"), data.get(
            "Data"), data.get("Header")
        if login_user=='user2':
            access_token=self.access_token2
        elif login_user=='user3':
            access_token=self.access_token3
        elif login_user=='user4':
            access_token=self.access_token4
        elif login_user=='user5':
            access_token=self.access_token5
        else:
            access_token  = self.access_token
        auth_dic = {"Cookie": f"access_token={access_token}"}
        conf.headers.update(_headers)
        print("测试111",conf.headers.update(_headers))
        conf.headers.update(auth_dic)
        print("测试222", conf.headers.update(auth_dic))
        _url = urljoin(f"{_scheme}://{conf.Host}", _url)
        #print(_url, _scheme, _method, _data, conf.headers)
        try:
            r = getattr(WebRequest(), _method.lower())(url=_url, data=json.dumps(_data), headers=conf.headers)
            with allure.step('步骤： 获取“{step}”接口response'.format(step=self.step)):
                allure.attach(_url, "Url")
                allure.attach(json.dumps(conf.headers), "headers")
                allure.attach(json.dumps(_data), "Data")
                allure.attach(r.text, "response")
            return r
        except Exception as e:
            #print(e)
            #raise EOFError(f"请求方式“{_method}”不正确，暂时不支持此方式")
            raise  EOFError(F'{e}')


if __name__ == '__main__':
    pass