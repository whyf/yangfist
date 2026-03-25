from public.import_module import ImportModule
from utils.log_utils import logger
from multiprocessing.dummy import Pool,Lock
import os,json

path = os.path.dirname(__file__)


class Auth():
    """
    因为这里设计的是单例模式，在conftest check_token的时候实例化传入了无效的token 当前进程中再次实例化就一直取的之前的，所以单例模式需要区分参数
    """
    #装实例化对象，相同参数的实例化共用一个实例化对象
    arg ={}

    #多线程锁
    _instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        相同参数共用一个实例化对象
        :param args:
        :param kwargs:
        :return:
        """
        key = str(args)+str(sorted(kwargs.items()))
        if key in Auth.arg.keys():
            return Auth.arg.get(key)
        with cls._instance_lock:
            Auth.arg[key] = object.__new__(cls)
            return Auth.arg.get(key)

    def __init__(self, login_data1:dict,login_data2:dict,login_data3:dict,login_data4:dict,login_data5:dict):
        #用户1的认证以及信息

        self.access_token = login_data1.get('access_token')
        self.access_token2=login_data2.get('access_token')
        self.access_token3=login_data3.get('access_token')
        self.access_token4=login_data4.get('access_token')
        self.access_token5=login_data5.get('access_token')

    def __getattribute__(self, attr):
        """

        :param attr:
        :return:
        """
        if attr.endswith('Module'):
            _class_module = ImportModule.import_module(attr)
            return _class_module(self.access_token,self.access_token2,self.access_token3,self.access_token4,self.access_token5)
        else:
            #非过滤直接访问
            return object.__getattribute__(self, attr)

if __name__ == '__main__':
    pass

